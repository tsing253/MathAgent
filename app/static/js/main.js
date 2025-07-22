document.addEventListener('DOMContentLoaded', function() {
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
    
    // 从sessionStorage获取用户信息
    const displayName = sessionStorage.getItem('name') || '用户';  // 使用name字段作为显示名
    const role = sessionStorage.getItem('role') || 'teacher';
    
    // 设置用户名显示
    usernameDisplay.textContent = displayName;
    
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
        sessionStorage.clear();  // 清除所有session数据
        
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
    async function loadHistory() {
        try {
            const response = await fetch('/get_conversations/');
            if (!response.ok) {
                throw new Error('获取历史记录失败');
            }
            
            const data = await response.json();
            historyList.innerHTML = '';
            
            if (data.conversations.length === 0) {
                historyList.innerHTML = '<li class="history-item empty">暂无历史会话</li>';
                return;
            }
            
            data.conversations.forEach(item => {
                const li = document.createElement('li');
                li.className = 'history-item';
                li.dataset.conversationId = item.coze_conversation_id;
                li.innerHTML = `
                    <div class="history-title" title="双击编辑标题">${item.title}</div>
                    <div class="history-date">${item.updated_at}</div>
                `;
                
                // 双击编辑标题
                const titleDiv = li.querySelector('.history-title');
                titleDiv.addEventListener('dblclick', async function(e) {
                    const currentTitle = this.textContent;
                    const input = document.createElement('input');
                    input.type = 'text';
                    input.value = currentTitle;
                    input.className = 'title-edit';
                    
                    this.replaceWith(input);
                    input.focus();
                    
                    input.addEventListener('blur', async function() {
                        const newTitle = this.value.trim();
                        if (newTitle && newTitle !== currentTitle) {
                            try {
                                const response = await fetch(`/conversation/${item.id}/update_title/`, {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({ title: newTitle })
                                });
                                
                                if (!response.ok) {
                                    throw new Error('更新标题失败');
                                }
                                
                                titleDiv.textContent = newTitle;
                            } catch (error) {
                                console.error('更新标题失败:', error);
                                titleDiv.textContent = currentTitle;
                            }
                        } else {
                            titleDiv.textContent = currentTitle;
                        }
                        this.replaceWith(titleDiv);
                    });
                    
                    input.addEventListener('keydown', function(e) {
                        if (e.key === 'Enter') {
                            this.blur();
                        } else if (e.key === 'Escape') {
                            titleDiv.textContent = currentTitle;
                            this.replaceWith(titleDiv);
                        }
                    });
                });
                
                historyList.appendChild(li);
            });
        } catch (error) {
            console.error('加载历史记录失败:', error);
            historyList.innerHTML = '<li class="history-item error">加载历史记录失败</li>';
        }
    }
    // 当前会话ID
    let currentConversationId = null;
    
    // 发送消息到后端API
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
            // 发送请求到后端API
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // 获取CSRF token
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: currentConversationId // 如果有当前会话ID则传递
                })
            });
            
            if (!response.ok) {
                throw new Error('请求失败，状态码: ' + response.status);
            }
            
            // 移除加载动画
            chatMessages.removeChild(loading);
            
            // 处理流式响应
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let aiMessage = '';
            let isFirstChunk = true;
            
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                aiMessage += chunk;
                
                // 更新AI消息显示
                if (isFirstChunk) {
                    addMessage(aiMessage, 'ai');
                    isFirstChunk = false;
                } else {
                    // 更新最后一个AI消息
                    const aiMessages = document.querySelectorAll('.ai-message');
                    const lastAiMessage = aiMessages[aiMessages.length - 1];
                    if (lastAiMessage) {
                        lastAiMessage.querySelector('div:last-child').innerHTML = aiMessage;
                    }
                }
                
                // 滚动到底部
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                // 重新渲染数学公式
                if (typeof MathJax !== 'undefined') {
                    MathJax.typeset();
                }
            }
            
            // 从响应头获取会话ID
            const newConversationId = response.headers.get('X-Conversation-ID');
            if (newConversationId) {
                currentConversationId = newConversationId;
                
                // 如果是新会话，添加到历史记录
                if (isFirstChunk) {
                    addNewConversationToHistory(newConversationId, message);
                }
            }
            
        } catch (error) {
            console.error('发送消息失败:', error);
            chatMessages.removeChild(loading);
            addMessage(`请求失败: ${error.message}`, 'ai');
        }
    }
    
    // 添加新会话到历史记录
    function addNewConversationToHistory(conversationId, firstMessage) {
        const now = new Date();
        const formattedDate = `${now.getFullYear()}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
        
        // 创建标题（截取前20个字符）
        const title = firstMessage.length > 20 ? firstMessage.substring(0, 20) + '...' : firstMessage;
        
        const li = document.createElement('li');
        li.className = 'history-item active';
        li.dataset.conversationId = conversationId;
        li.innerHTML = `
            <div class="history-title" title="双击编辑标题">${title}</div>
            <div class="history-date">${formattedDate}</div>
        `;
        
        // 添加点击事件
        li.addEventListener('click', function() {
            document.querySelectorAll('.history-item').forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            loadConversation(conversationId);
        });
        
        // 添加到历史记录顶部
        if (historyList.querySelector('.empty')) {
            historyList.innerHTML = '';
        }
        historyList.insertBefore(li, historyList.firstChild);
        
        // 更新当前会话ID
        currentConversationId = conversationId;
    }
    
    // 获取CSRF token的函数
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // 添加消息到聊天区域
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="message-header">
                    <i class="fas fa-user"></i>${displayName}
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
            addMessage(`欢迎回来，${displayName}${role === 'teacher' ? '老师' : '同学'}！今天想学习什么内容？`, 'ai');
        }, 500);
    }
    
    // 初始化页面
    initPage();
});