import os

ADMIN_FILE = r'C:\Users\xingk\Lloyds Banking Group\admin.html'

with open(ADMIN_FILE, 'r', encoding='utf-8') as f:
    admin_html = f.read()

# Replace HTML for profile pic
old_html = """                <!-- Profile Picture -->
                <div class="settings-group">
                    <p><i class="fas fa-image"></i> Victim Profile Picture</p>
                    <input type="text" id="adminProfilePic" placeholder="Image URL (e.g. https://...)">
                    <button id="btnUpdateProfilePic">Update Profile Picture</button>
                    <div id="profilePicStatus" class="status-msg"></div>
                </div>"""

new_html = """                <!-- Profile Picture -->
                <div class="settings-group">
                    <p><i class="fas fa-image"></i> Victim Profile Picture</p>
                    <input type="file" id="adminProfilePicFile" accept="image/*" style="background:#151521; padding:8px; width:100%; color:white; border:1px solid #3a3a52; border-radius:4px; margin-bottom:8px;">
                    <button id="btnUpdateProfilePic">Upload Profile Picture</button>
                    <div id="profilePicStatus" class="status-msg"></div>
                </div>"""

admin_html = admin_html.replace(old_html, new_html)

# Replace JS logic
old_js = """        // Update Profile Picture
        var btnUpdateProfilePic = document.getElementById('btnUpdateProfilePic');
        if (btnUpdateProfilePic) {
            btnUpdateProfilePic.addEventListener('click', async function() {
                var url = document.getElementById('adminProfilePic').value.trim();
                if (url) await setSyncItem('profilePic', url);
                document.getElementById('profilePicStatus').innerText = 'Profile picture updated!';
                setTimeout(function(){ document.getElementById('profilePicStatus').innerText = ''; }, 3000);
            });
        }"""

new_js = """        // Update Profile Picture (Upload)
        var btnUpdateProfilePic = document.getElementById('btnUpdateProfilePic');
        if (btnUpdateProfilePic) {
            btnUpdateProfilePic.addEventListener('click', function() {
                var fileInput = document.getElementById('adminProfilePicFile');
                if (fileInput.files && fileInput.files[0]) {
                    var reader = new FileReader();
                    reader.onload = async function(e) {
                        var base64Image = e.target.result;
                        await setSyncItem('profilePic', base64Image);
                        document.getElementById('profilePicStatus').innerText = 'Profile picture uploaded and updated!';
                        setTimeout(function(){ document.getElementById('profilePicStatus').innerText = ''; }, 3000);
                    };
                    reader.readAsDataURL(fileInput.files[0]);
                } else {
                    alert('Please select an image file to upload.');
                }
            });
        }"""

admin_html = admin_html.replace(old_js, new_js)

# Also remove the polling logic that tries to set the value of the non-existent text input
old_poll_js = """            // Poll Profile Picture
            var pPic = getSyncItem('profilePic');
            if (pPic && document.activeElement !== document.getElementById('adminProfilePic')) {
                var adminPicEl = document.getElementById('adminProfilePic');
                if(adminPicEl) adminPicEl.value = pPic;
            }"""

new_poll_js = """            // Poll Profile Picture (File input cannot be populated programmatically for security reasons, so we skip it)
            var pPic = getSyncItem('profilePic');"""

admin_html = admin_html.replace(old_poll_js, new_poll_js)

with open(ADMIN_FILE, 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Profile picture upload logic injected successfully.")
