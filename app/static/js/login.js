document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');  // 获取表单元素
    const loginBtn = document.getElementById('loginBtn');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const registerLink = document.getElementById('registerLink');
    const forgotPassword = document.getElementById('forgotPassword');

    // 表单提交事件
    loginForm.addEventListener('submit', function(e) {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        
        if (!username || !password) {
            e.preventDefault();  // 阻止表单提交
            showNotification('请输入用户名和密码', 'error');
            return false;
        }
        
        // 显示加载效果
        loginBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 登录中...';
        loginBtn.disabled = true;
        
    });

    // 显示通知函数
    function showNotification(message, type) {
        // 移除现有通知
        const existingNotif = document.querySelector('.notification');
        if (existingNotif) existingNotif.remove();
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${message}
        `;
        
        document.body.appendChild(notification);
        
        // 3秒后移除通知
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
});