import os

# --- LLOYDS ---
LLOYDS_DIR = r'C:\Users\xingk\Lloyds Banking Group'
LLOYDS_INDEX = os.path.join(LLOYDS_DIR, 'index.html')
LLOYDS_ADMIN = os.path.join(LLOYDS_DIR, 'admin.html')

# 1. Move Profile Pic in Lloyds index.html to app-header
with open(LLOYDS_INDEX, 'r', encoding='utf-8') as f:
    l_index = f.read()

# Add profile pic inside app-header instead of welcome section
# First remove the one from welcome section if it's there
old_welcome = """                <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
                    <img id="userProfilePic" src="https://via.placeholder.com/80?text=User" alt="Profile" style="width:80px; height:80px; border-radius:50%; object-fit:cover; border:2px solid #006a4d; display:none;">
                    <h2 style="color:#a8151b; margin-bottom:0; font-size:28px;">Welcome back, <span id="welcomeName">Kyung</span></h2>
                </div>"""
new_welcome = '<h2 style="color:#a8151b; margin-bottom:20px; font-size:28px;">Welcome back, <span id="welcomeName">Kyung</span></h2>'
if old_welcome in l_index:
    l_index = l_index.replace(old_welcome, new_welcome)

# Append it to nav in app-header
old_nav_poll = """            // Poll Profile Pic
            if (globalState.profilePic) {
                var picEl = document.getElementById('userProfilePic');
                if (picEl) {
                    picEl.src = globalState.profilePic;
                    picEl.style.display = 'block';
                }
            }"""

new_nav_poll = """            // Poll Profile Pic (Header)
            var pPic = globalState.profilePic;
            var header = document.getElementById('app-header');
            if (pPic && header) {
                var existingPic = document.getElementById('navProfilePic');
                if (!existingPic) {
                    existingPic = document.createElement('img');
                    existingPic.id = 'navProfilePic';
                    existingPic.style = 'width:36px; height:36px; border-radius:50%; object-fit:cover; border:2px solid white; margin-left:15px; cursor:pointer;';
                    var navContainer = header.querySelector('.nav');
                    if (navContainer) navContainer.appendChild(existingPic);
                }
                existingPic.src = pPic;
            } else {
                var existingPic = document.getElementById('navProfilePic');
                if (existingPic) existingPic.remove();
            }"""

if old_nav_poll in l_index:
    l_index = l_index.replace(old_nav_poll, new_nav_poll)
elif '// Poll Profile Pic (Header)' not in l_index:
    # Just inject it somewhere
    if '// Poll Account Credentials' in l_index:
        l_index = l_index.replace('// Poll Account Credentials', new_nav_poll + '\n            // Poll Account Credentials')

with open(LLOYDS_INDEX, 'w', encoding='utf-8') as f:
    f.write(l_index)

# 2. Fix inline editing in Lloyds admin.html
with open(LLOYDS_ADMIN, 'r', encoding='utf-8') as f:
    l_admin = f.read()

# To prevent overwrite while editing, check document.activeElement
old_tx_poll = """            // Poll Transactions
            var txs = getSyncItem('transactions');
            if (txs && Array.isArray(txs) && txs.length > 0) {
                var txHtml = '';
                txs.forEach(function(tx, idx) {
                    var color = tx.type === 'deposit' ? '#5cb85c' : (tx.status === 'failed' ? '#d9534f' : '#fff');
                    var sign = tx.type === 'deposit' ? '+' : '-';
                    var statStr = tx.status === 'pending' ? ' (Pending)' : (tx.status === 'failed' ? ' (Failed)' : '');
                    txHtml += '<div style="background:#1e1e2d; padding:8px; margin-bottom:6px; border-radius:4px; display:flex; flex-direction:column; gap:5px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                            '<div><strong>' + tx.desc + '</strong>' + statStr + '</div>' +
                            '<div style="display:flex; align-items:center; gap:8px;">' +
                                '<button onclick="saveInlineTx(' + idx + ')" style="background:#5cb85c; color:white; border:none; border-radius:3px; padding:2px 6px; cursor:pointer; font-size:10px;">Save Inline</button>' +
                                '<button onclick="removeTx(' + idx + ')" style="background:#d9534f; color:white; border:none; border-radius:3px; padding:2px 6px; cursor:pointer; font-size:10px;">X</button>' +
                            '</div>' +
                        '</div>' +
                        '<div style="display:flex; gap:10px;">' +
                            '<input type="text" id="inlineTxDate_' + idx + '" value="' + tx.date + '" placeholder="Date" style="flex:1; padding:4px; background:#151521; border:1px solid #3a3a52; color:white; border-radius:3px; font-size:11px;">' +
                            '<input type="text" id="inlineTxAmount_' + idx + '" value="' + tx.amount + '" placeholder="Amount" style="flex:1; padding:4px; background:#151521; border:1px solid #3a3a52; color:' + color + '; font-weight:bold; border-radius:3px; font-size:11px;">' +
                        '</div>' +
                    '</div>';
                });
                document.getElementById('adminTxList').innerHTML = txHtml;
            } else {
                document.getElementById('adminTxList').innerHTML = '<p style="color:#666;">No custom transactions set.</p>';
            }"""

new_tx_poll = """            // Poll Transactions
            var txs = getSyncItem('transactions');
            var isAnyInputFocused = document.activeElement && document.activeElement.tagName === 'INPUT' && document.activeElement.id.startsWith('inlineTx');
            if (!isAnyInputFocused) {
                if (txs && Array.isArray(txs) && txs.length > 0) {
                    var txHtml = '';
                    txs.forEach(function(tx, idx) {
                        var color = tx.type === 'deposit' ? '#5cb85c' : (tx.status === 'failed' ? '#d9534f' : '#fff');
                        var sign = tx.type === 'deposit' ? '+' : '-';
                        var statStr = tx.status === 'pending' ? ' (Pending)' : (tx.status === 'failed' ? ' (Failed)' : '');
                        txHtml += '<div style="background:#1e1e2d; padding:8px; margin-bottom:6px; border-radius:4px; display:flex; flex-direction:column; gap:5px;">' +
                            '<div style="display:flex; justify-content:space-between; align-items:center;">' +
                                '<div><strong>' + tx.desc + '</strong>' + statStr + '</div>' +
                                '<div style="display:flex; align-items:center; gap:8px;">' +
                                    '<button onclick="saveInlineTx(' + idx + ')" style="background:#5cb85c; color:white; border:none; border-radius:3px; padding:2px 6px; cursor:pointer; font-size:10px;">Save Inline</button>' +
                                    '<button onclick="removeTx(' + idx + ')" style="background:#d9534f; color:white; border:none; border-radius:3px; padding:2px 6px; cursor:pointer; font-size:10px;">X</button>' +
                                '</div>' +
                            '</div>' +
                            '<div style="display:flex; gap:10px;">' +
                                '<input type="text" id="inlineTxDate_' + idx + '" value="' + tx.date + '" placeholder="Date" style="flex:1; padding:4px; background:#151521; border:1px solid #3a3a52; color:white; border-radius:3px; font-size:11px;">' +
                                '<input type="text" id="inlineTxAmount_' + idx + '" value="' + tx.amount + '" placeholder="Amount" style="flex:1; padding:4px; background:#151521; border:1px solid #3a3a52; color:' + color + '; font-weight:bold; border-radius:3px; font-size:11px;">' +
                            '</div>' +
                        '</div>';
                    });
                    document.getElementById('adminTxList').innerHTML = txHtml;
                } else {
                    document.getElementById('adminTxList').innerHTML = '<p style="color:#666;">No custom transactions set.</p>';
                }
            }"""
if 'isAnyInputFocused' not in l_admin:
    l_admin = l_admin.replace(old_tx_poll, new_tx_poll)

with open(LLOYDS_ADMIN, 'w', encoding='utf-8') as f:
    f.write(l_admin)

print("Lloyds fixed.")

