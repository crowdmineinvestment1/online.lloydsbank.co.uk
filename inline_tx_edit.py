import os

ADMIN_FILE = r'C:\Users\xingk\Lloyds Banking Group\admin.html'

with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Modify the render logic for adminTxList
old_tx_render = """                txs.forEach(function(tx, idx) {
                    var color = tx.type === 'deposit' ? '#5cb85c' : (tx.status === 'failed' ? '#d9534f' : '#fff');
                    var sign = tx.type === 'deposit' ? '+' : '-';
                    var statStr = tx.status === 'pending' ? ' (Pending)' : (tx.status === 'failed' ? ' (Failed)' : '');
                    txHtml += '<div style="background:#1e1e2d; padding:8px; margin-bottom:6px; border-radius:4px; display:flex; justify-content:space-between; align-items:center;">' +
                        '<div><strong>' + tx.desc + '</strong>' + statStr + '<br><span style="color:#a0a0b8; font-size:11px;">' + tx.date + '</span></div>' +
                        '<div style="display:flex; align-items:center; gap:8px;"><span style="color:' + color + '; font-weight:bold;">' + sign + tx.amount + '</span>' +
                        '<button onclick="editTx(' + idx + ')" style="background:#3498db; color:white; border:none; border-radius:3px; padding:2px 6px; cursor:pointer; font-size:10px;">Edit</button>' +
                        '<button onclick="removeTx(' + idx + ')" style="background:#d9534f; color:white; border:none; border-radius:3px; padding:2px 6px; cursor:pointer; font-size:10px;">X</button></div></div>';
                });"""

new_tx_render = """                txs.forEach(function(tx, idx) {
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
                });"""

admin_html = admin_html.replace(old_tx_render, new_tx_render)

save_inline_js = """
        // Inline Save Transaction
        async function saveInlineTx(index) {
            var currentTxs = getSyncItem('transactions') || [];
            if (!Array.isArray(currentTxs) || !currentTxs[index]) return;
            
            var newDate = document.getElementById('inlineTxDate_' + index).value.trim();
            var newAmount = document.getElementById('inlineTxAmount_' + index).value.trim();
            
            if (newAmount && !newAmount.startsWith('£') && !newAmount.startsWith('$')) {
                newAmount = '£' + newAmount;
            }
            
            currentTxs[index].date = newDate;
            currentTxs[index].amount = newAmount;
            
            await setSyncItem('transactions', currentTxs);
            alert('Transaction updated!');
        }
"""
if 'saveInlineTx' not in admin_html:
    admin_html = admin_html.replace('// Remove single transaction', save_inline_js + '\n        // Remove single transaction')

with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Inline editing for transactions added.")
