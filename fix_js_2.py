import re

INDEX_FILE = 'C:\\Users\\xingk\\Lloyds Banking Group\\index.html'

with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    index_html = f.read()

# I will replace the messy originalShowView logic and handleQuickAction with a clean version.
# I will find the handleQuickAction function block and the showView function block.

# First, find the original showView (lines 660ish)
old_show_view = '''        function showView(viewId) {
            document.getElementById('view-login').style.display = 'none';
            document.getElementById('app-header').style.display = 'flex';
            document.getElementById('main-app').style.display = 'flex';

            document.getElementById('view-home').style.display = 'none';
            document.getElementById('view-verification').style.display = 'none';
            document.getElementById('view-history').style.display = 'none';

            var el = document.getElementById('view-' + viewId);
            if (el) {
                el.style.display = (viewId === 'verification') ? 'flex' : 'block';
            }
        }'''

new_show_view = '''        function showView(viewId) {
            try {
                var elsToHide = ['view-login', 'view-home', 'view-verification', 'view-history', 'view-transfer', 'view-bills', 'view-investments'];
                for (var i=0; i<elsToHide.length; i++) {
                    var el = document.getElementById(elsToHide[i]);
                    if (el) el.style.display = 'none';
                }

                var header = document.getElementById('app-header');
                if (header) header.style.display = 'flex';
                
                var mainApp = document.getElementById('main-app');
                if (mainApp) mainApp.style.display = 'flex';

                var target = document.getElementById('view-' + viewId);
                if (target) {
                    target.style.display = (viewId === 'verification') ? 'flex' : 'block';
                }
            } catch(e) {
                alert("Error in showView: " + e.message);
            }
        }'''

index_html = index_html.replace(old_show_view, new_show_view)


# Next, find the hacky showView overriding and handleQuickAction
hacky_js_start = '// ===== DYNAMIC ACCOUNT STATUS ====='
hacky_js_end = '// Bank List Data'

if hacky_js_start in index_html and hacky_js_end in index_html:
    part1 = index_html.split(hacky_js_start)[0]
    part2 = index_html.split(hacky_js_end)[1]

    new_middle = '''// ===== DYNAMIC ACCOUNT STATUS =====
        var localAccountLocked = false;
        
        function handleQuickAction(action) {
            try {
                if (localAccountLocked) {
                    showAccountClosedAlert();
                } else {
                    if (action === 'transfer') initTransferBanks();
                    showView(action);
                }
            } catch(e) {
                alert("Error in handleQuickAction: " + e.message);
            }
        }

        // Bank List Data'''

    index_html = part1 + new_middle + part2


with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(index_html)

print("Rewrote showView and handleQuickAction.")
