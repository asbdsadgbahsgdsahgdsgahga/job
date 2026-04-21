<?php
session_start();

// Database configuration
$db_host = 'localhost';
$db_name = 'institution_db';
$db_user = 'root';
$db_pass = '';

try {
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    die("Connection failed: " . $e->getMessage());
}

// Authentication
function isLoggedIn() {
    return isset($_SESSION['admin_logged_in']) && $_SESSION['admin_logged_in'] === true;
}

function login($username, $password) {
    global $pdo;
    
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND role = 'admin'");
    $stmt->execute([$username]);
    $user = $stmt->fetch();
    
    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['admin_logged_in'] = true;
        $_SESSION['admin_id'] = $user['id'];
        $_SESSION['admin_username'] = $user['username'];
        return true;
    }
    return false;
}

function logout() {
    session_destroy();
    header('Location: admin.php');
    exit();
}

// Handle login
if ($_POST && isset($_POST['action']) && $_POST['action'] === 'login') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    
    if (login($username, $password)) {
        header('Location: admin.php');
        exit();
    } else {
        $error = "Invalid credentials";
    }
}

// Handle logout
if (isset($_GET['logout'])) {
    logout();
}

// API endpoints for AJAX requests
if (isset($_GET['api'])) {
    header('Content-Type: application/json');
    
    if (!isLoggedIn()) {
        http_response_code(401);
        echo json_encode(['error' => 'Unauthorized']);
        exit();
    }
    
    switch ($_GET['api']) {
        case 'admissions':
            $stmt = $pdo->query("SELECT * FROM admissions ORDER BY created_at DESC");
            echo json_encode($stmt->fetchAll());
            break;
            
        case 'messages':
            $stmt = $pdo->query("SELECT * FROM contact_messages ORDER BY created_at DESC");
            echo json_encode($stmt->fetchAll());
            break;
            
        case 'stats':
            $stats = [];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM admissions");
            $stats['admissions'] = $stmt->fetch()['count'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM contact_messages");
            $stats['messages'] = $stmt->fetch()['count'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM programs WHERE is_active = 1");
            $stats['programs'] = $stmt->fetch()['count'];
            
            $stmt = $pdo->query("SELECT COUNT(*) as count FROM faculty WHERE is_active = 1");
            $stats['faculty'] = $stmt->fetch()['count'];
            
            echo json_encode($stats);
            break;
            
        case 'add_program':
            $data = json_decode(file_get_contents('php://input'), true);
            
            $stmt = $pdo->prepare("INSERT INTO programs (name, description, duration, category) VALUES (?, ?, ?, ?)");
            $stmt->execute([
                $data['name'],
                $data['description'],
                $data['duration'],
                $data['category']
            ]);
            
            echo json_encode(['message' => 'Program added successfully']);
            break;
            
        case 'add_faculty':
            $data = json_decode(file_get_contents('php://input'), true);
            
            $stmt = $pdo->prepare("INSERT INTO faculty (name, title, department, bio, email, image_url) VALUES (?, ?, ?, ?, ?, ?)");
            $stmt->execute([
                $data['name'],
                $data['title'],
                $data['department'],
                $data['bio'] ?? '',
                $data['email'] ?? '',
                $data['image_url'] ?? ''
            ]);
            
            echo json_encode(['message' => 'Faculty member added successfully']);
            break;
            
        default:
            http_response_code(404);
            echo json_encode(['error' => 'API endpoint not found']);
    }
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - Your Institution</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: #f8f9fa;
            color: #333;
        }
        
        .admin-container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 250px;
            background: #2c3e50;
            color: white;
            padding: 20px 0;
        }
        
        .sidebar-header {
            padding: 0 20px 20px;
            border-bottom: 1px solid #34495e;
        }
        
        .sidebar-header h2 {
            color: #3498db;
        }
        
        .nav-menu {
            list-style: none;
            padding: 20px 0;
        }
        
        .nav-item {
            margin-bottom: 5px;
        }
        
        .nav-link {
            display: block;
            padding: 12px 20px;
            color: #bdc3c7;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .nav-link:hover,
        .nav-link.active {
            background: #34495e;
            color: #3498db;
        }
        
        .nav-link i {
            margin-right: 10px;
            width: 20px;
        }
        
        .main-content {
            flex: 1;
            padding: 20px;
        }
        
        .header {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            color: #2c3e50;
        }
        
        .logout-btn {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            transition: background 0.3s ease;
        }
        
        .logout-btn:hover {
            background: #c0392b;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .stat-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #3498db;
        }
        
        .content-section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .section-title {
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .table th,
        .table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .btn {
            display: inline-block;
            padding: 8px 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-primary:hover {
            background: #2980b9;
        }
        
        .btn-success {
            background: #27ae60;
            color: white;
        }
        
        .btn-success:hover {
            background: #229954;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c0392b;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #2c3e50;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 100px;
        }
        
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .login-form {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        
        .login-form h2 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        
        .error {
            background: #e74c3c;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .hidden {
            display: none;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
    </style>
</head>
<body>
    <?php if (!isLoggedIn()): ?>
    <!-- Login Form -->
    <div class="login-container">
        <div class="login-form">
            <h2>Admin Login</h2>
            <?php if (isset($error)): ?>
                <div class="error"><?php echo $error; ?></div>
            <?php endif; ?>
            <form method="POST">
                <input type="hidden" name="action" value="login">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary" style="width: 100%;">Login</button>
            </form>
        </div>
    </div>
    <?php else: ?>
    <!-- Admin Dashboard -->
    <div class="admin-container">
        <div class="sidebar">
            <div class="sidebar-header">
                <h2>Admin Panel</h2>
            </div>
            <ul class="nav-menu">
                <li class="nav-item">
                    <a href="#dashboard" class="nav-link active" data-tab="dashboard">
                        <i class="fas fa-tachometer-alt"></i> Dashboard
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#admissions" class="nav-link" data-tab="admissions">
                        <i class="fas fa-user-graduate"></i> Admissions
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#messages" class="nav-link" data-tab="messages">
                        <i class="fas fa-envelope"></i> Messages
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#programs" class="nav-link" data-tab="programs">
                        <i class="fas fa-book"></i> Programs
                    </a>
                </li>
                <li class="nav-item">
                    <a href="#faculty" class="nav-link" data-tab="faculty">
                        <i class="fas fa-users"></i> Faculty
                    </a>
                </li>
            </ul>
        </div>
        
        <div class="main-content">
            <div class="header">
                <h1>Welcome, <?php echo htmlspecialchars($_SESSION['admin_username']); ?></h1>
                <a href="?logout=1" class="logout-btn">Logout</a>
            </div>
            
            <!-- Dashboard Tab -->
            <div id="dashboard" class="tab-content active">
                <div class="dashboard-grid">
                    <div class="stat-card">
                        <h3>Total Admissions</h3>
                        <div class="stat-number" id="admissions-count">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Contact Messages</h3>
                        <div class="stat-number" id="messages-count">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Active Programs</h3>
                        <div class="stat-number" id="programs-count">-</div>
                    </div>
                    <div class="stat-card">
                        <h3>Faculty Members</h3>
                        <div class="stat-number" id="faculty-count">-</div>
                    </div>
                </div>
            </div>
            
            <!-- Admissions Tab -->
            <div id="admissions" class="tab-content">
                <div class="content-section">
                    <h2 class="section-title">Admission Applications</h2>
                    <div id="admissions-table"></div>
                </div>
            </div>
            
            <!-- Messages Tab -->
            <div id="messages" class="tab-content">
                <div class="content-section">
                    <h2 class="section-title">Contact Messages</h2>
                    <div id="messages-table"></div>
                </div>
            </div>
            
            <!-- Programs Tab -->
            <div id="programs" class="tab-content">
                <div class="content-section">
                    <h2 class="section-title">Add New Program</h2>
                    <form id="program-form">
                        <div class="form-group">
                            <label for="program-name">Program Name</label>
                            <input type="text" id="program-name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="program-description">Description</label>
                            <textarea id="program-description" name="description" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="program-duration">Duration</label>
                            <input type="text" id="program-duration" name="duration" placeholder="e.g., 4 years" required>
                        </div>
                        <div class="form-group">
                            <label for="program-category">Category</label>
                            <select id="program-category" name="category" required>
                                <option value="">Select Category</option>
                                <option value="undergraduate">Undergraduate</option>
                                <option value="graduate">Graduate</option>
                                <option value="online">Online Learning</option>
                                <option value="professional">Professional Development</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Add Program</button>
                    </form>
                </div>
            </div>
            
            <!-- Faculty Tab -->
            <div id="faculty" class="tab-content">
                <div class="content-section">
                    <h2 class="section-title">Add New Faculty Member</h2>
                    <form id="faculty-form">
                        <div class="form-group">
                            <label for="faculty-name">Name</label>
                            <input type="text" id="faculty-name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="faculty-title">Title</label>
                            <input type="text" id="faculty-title" name="title" required>
                        </div>
                        <div class="form-group">
                            <label for="faculty-department">Department</label>
                            <input type="text" id="faculty-department" name="department" required>
                        </div>
                        <div class="form-group">
                            <label for="faculty-bio">Bio</label>
                            <textarea id="faculty-bio" name="bio"></textarea>
                        </div>
                        <div class="form-group">
                            <label for="faculty-email">Email</label>
                            <input type="email" id="faculty-email" name="email">
                        </div>
                        <div class="form-group">
                            <label for="faculty-image">Image URL</label>
                            <input type="url" id="faculty-image" name="image_url">
                        </div>
                        <button type="submit" class="btn btn-primary">Add Faculty Member</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Tab switching
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all links and tabs
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked link
                this.classList.add('active');
                
                // Show corresponding tab
                const tabId = this.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
                
                // Load data for the tab
                loadTabData(tabId);
            });
        });
        
        // Load dashboard stats
        function loadDashboardStats() {
            fetch('?api=stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('admissions-count').textContent = data.admissions;
                    document.getElementById('messages-count').textContent = data.messages;
                    document.getElementById('programs-count').textContent = data.programs;
                    document.getElementById('faculty-count').textContent = data.faculty;
                })
                .catch(error => console.error('Error loading stats:', error));
        }
        
        // Load tab data
        function loadTabData(tabId) {
            switch(tabId) {
                case 'admissions':
                    loadAdmissions();
                    break;
                case 'messages':
                    loadMessages();
                    break;
            }
        }
        
        // Load admissions data
        function loadAdmissions() {
            fetch('?api=admissions')
                .then(response => response.json())
                .then(data => {
                    const table = document.getElementById('admissions-table');
                    table.innerHTML = `
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Program</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.map(admission => `
                                    <tr>
                                        <td>${admission.name}</td>
                                        <td>${admission.email}</td>
                                        <td>${admission.phone}</td>
                                        <td>${admission.program}</td>
                                        <td>${new Date(admission.created_at).toLocaleDateString()}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `;
                })
                .catch(error => console.error('Error loading admissions:', error));
        }
        
        // Load messages data
        function loadMessages() {
            fetch('?api=messages')
                .then(response => response.json())
                .then(data => {
                    const table = document.getElementById('messages-table');
                    table.innerHTML = `
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Subject</th>
                                    <th>Message</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.map(message => `
                                    <tr>
                                        <td>${message.name}</td>
                                        <td>${message.email}</td>
                                        <td>${message.subject}</td>
                                        <td>${message.message.substring(0, 50)}...</td>
                                        <td>${new Date(message.created_at).toLocaleDateString()}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    `;
                })
                .catch(error => console.error('Error loading messages:', error));
        }
        
        // Handle program form submission
        document.getElementById('program-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('?api=add_program', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                this.reset();
                loadDashboardStats();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding program');
            });
        });
        
        // Handle faculty form submission
        document.getElementById('faculty-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('?api=add_faculty', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                this.reset();
                loadDashboardStats();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding faculty member');
            });
        });
        
        // Load initial data
        loadDashboardStats();
    </script>
    <?php endif; ?>
</body>
</html> 