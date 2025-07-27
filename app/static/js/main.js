document.addEventListener('DOMContentLoaded', function() {
    // 从 sessionStorage 获取用户名和角色
    const username = sessionStorage.getItem('username') || '用户';
    const role = sessionStorage.getItem('role') || 'student';

    // 获取页面元素
    const logoutBtn = document.getElementById('logoutBtn');
    const teacherBtn = document.getElementById('teacherBtn');
    const studentBtn = document.getElementById('studentBtn');
    const functionList = document.getElementById('functionList');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const chatMessages = document.getElementById('chatMessages');
    const historyList = document.getElementById('historyList');
    const usernameDisplay = document.getElementById('usernameDisplay');
    
    // 学生功能列表
    const studentFunctions = [
        {icon: 'fas fa-book', name: '平时练习'},
        {icon: 'fas fa-robot', name: 'AI答疑'},
        {icon: 'fas fa-chart-pie', name: '学情分析'},
        {icon: 'fas fa-tasks', name: '作业中心'},
        {icon: 'fas fa-graduation-cap', name: '学习路径'}
    ];
    
    // 教师功能列表
    const teacherFunctions = [
        {icon: 'fas fa-question-circle', name: '智能出题'},
        {icon: 'fas fa-check-double', name: '辅助批卷'},
        {icon: 'fas fa-chart-line', name: '教学分析'},
        {icon: 'fas fa-book', name: '课程管理'},
        {icon: 'fas fa-users', name: '学生管理'}
    ];

    // 获取CSRF token的函数
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        if (cookieValue) return cookieValue;
        return document.querySelector('meta[name="csrf-token"]')?.content;
    }
    
    // 加载会话内容的函数
    async function loadConversation(conversationId) {
        try {
            // 显示加载中状态
            chatMessages.innerHTML = `
                <div class="loading">
                    <span>加载中</span>
                    <div class="loading-dots">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
            `;

            const response = await fetch(`/conversation/${conversationId}/`);
            if (!response.ok) {
                throw new Error('加载失败');
            }

            const data = await response.json();
            
            // 清空聊天区域
            chatMessages.innerHTML = '';
            
            // 添加所有对话内容
            data.dialogues.forEach(dialogue => {
                // 添加用户消息
                chatMessages.innerHTML += `
                    <div class="message user-message">
                        <div class="message-header">
                            <i class="fas fa-user"></i>我
                        </div>
                        <div>${dialogue.user_input}</div>
                    </div>
                `;
                
                // 添加AI响应
                chatMessages.innerHTML += `
                    <div class="message ai-message">
                        <div class="message-header">
                            <i class="fas fa-robot"></i>高数帮AI
                        </div>
                        <div>${dialogue.agent_output}</div>
                    </div>
                `;
            });

            // 滚动到底部
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
        } catch (error) {
            chatMessages.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-circle"></i>
                    加载会话内容失败，请重试
                </div>
            `;
        }
    }

    // 处理历史会话点击
    document.querySelectorAll('.history-item').forEach(item => {
        if (!item.classList.contains('empty')) {
            item.addEventListener('click', function() {
                const conversationId = this.dataset.conversationId;
                // 高亮当前选中的会话
                document.querySelectorAll('.history-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
                // 加载会话内容
                loadConversation(conversationId);
            });
        }
    });
    
    // 退出登录
    logoutBtn.addEventListener('click', function() {
        // 清除sessionStorage
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('role');
        
        // 跳转回登录页面
        window.location.href = '/login/';
    });
    
    // 身份切换功能
    teacherBtn.addEventListener('click', function() {
        teacherBtn.classList.add('active');
        studentBtn.classList.remove('active');
        updateFunctionList('teacher');
        sessionStorage.setItem('role', 'teacher');
    });
    
    studentBtn.addEventListener('click', function() {
        studentBtn.classList.add('active');
        teacherBtn.classList.remove('active');
        updateFunctionList('student');
        sessionStorage.setItem('role', 'student');
    });
    
    // 更新功能列表
    function updateFunctionList(role) {
        functionList.innerHTML = '';
        const functions = role === 'teacher' ? teacherFunctions : studentFunctions;
        
        functions.forEach(func => {
            const li = document.createElement('li');
            li.className = 'function-item';
            li.innerHTML = `
                <i class="${func.icon}"></i>${func.name}
            `;
            functionList.appendChild(li);
        });
    }
    
    // 加载历史记录
    function loadHistory() {
        historyList.innerHTML = '';
        
        historyData.forEach(item => {
            const li = document.createElement('li');
            li.className = 'history-item';
            li.innerHTML = `
                <div class="history-title">${item.title}</div>
                <div class="history-date">${item.date}</div>
            `;
            historyList.appendChild(li);
        });
    }
    
    // 发送消息 - 使用真实API
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // 添加用户消息
        addMessage(message, 'user');
        messageInput.value = '';
        
        // 显示加载动画
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerHTML = `
            <div>高数帮AI正在思考...</div>
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatMessages.appendChild(loading);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            // 创建AI消息容器
            const aiMessageDiv = document.createElement('div');
            aiMessageDiv.className = 'message ai-message';
            aiMessageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-robot"></i>高数帮AI
                </div>
                <div class="ai-content"></div>
            `;
            chatMessages.appendChild(aiMessageDiv);
            const aiContent = aiMessageDiv.querySelector('.ai-content');
            
            // 移除加载动画
            chatMessages.removeChild(loading);
            
            // 发送请求到代理API
            const formData = new FormData();
            formData.append('message', message);
            
            
            // 获取CSRF token
            const csrftoken = getCSRFToken();
            
            // 修改第一个POST请求（/api/coze-proxy/）
            const response = await fetch('/api/coze-proxy/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken  // 添加CSRF头
                },
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('API请求失败');
            }
            
            // 处理流式响应
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let aiResponse = '';
            
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                aiResponse += chunk;
                
                // 更新AI消息内容
                aiContent.innerHTML = aiResponse;
                
                // 滚动到底部
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
            
            // 保存对话到后端
            await fetch('/api/save-conversation/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken  // 添加CSRF头
                },
                body: JSON.stringify({
                    'user_input': message,
                    'agent_output': aiResponse
                })
            });
                
        } catch (error) {
            chatMessages.removeChild(loading);
            addMessage(`抱歉，请求出错: ${error.message}`, 'ai');
        }
    }
    
    // 添加消息到聊天区域
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-user"></i>${username}
                </div>
                <div>${content}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-robot"></i>高数帮AI
                </div>
                <div>${content}</div>
            `;
        }
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // 重新渲染数学公式
        if (typeof MathJax !== 'undefined') {
            MathJax.typeset();
        }
    }
    
    // 发送按钮事件
    sendBtn.addEventListener('click', sendMessage);
    
    // 按Enter发送消息（Shift+Enter换行）
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // 初始化页面
    function initPage() {
        // 设置角色
        if (role === 'student') {
            studentBtn.click();
        } else {
            teacherBtn.click();
        }
        
        // 加载历史记录
        loadHistory();
        
        // 添加欢迎消息
        setTimeout(() => {
            addMessage(`欢迎回来，${username}${role === 'teacher' ? '老师' : '同学'}！今天想学习什么内容？`, 'ai');
        }, 500);
    }
    
    // 初始化页面
    initPage();
});