<?php
// Include database connection
require_once 'connection.php';

// This script will update the admin password to "admin123"
// You can change this password below
$username = 'admin';
$new_password = 'admin1234';

// Hash the password using password_hash (PHP's recommended method)
$hashed_password = password_hash($new_password, PASSWORD_DEFAULT);

// Update the user's password in the database
$sql = "UPDATE users SET password = ? WHERE username = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $hashed_password, $username);

if ($stmt->execute()) {
    echo "Password for user '$username' has been reset to '$new_password'.<br>";
    echo "You can now login using these credentials.";
} else {
    echo "Error updating password: " . $conn->error;
}

$stmt->close();
$conn->close();
?>