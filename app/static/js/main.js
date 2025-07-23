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
    
    // 发送消息
    function sendMessage() {
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
        
        // 模拟AI响应
        setTimeout(() => {
            chatMessages.removeChild(loading);
            let response = '';
            
            if (message.includes('导数') || message.includes('微分')) {
                response = `关于导数/微分的问题，我为您提供以下解答：
                <div class="math-formula">
                    导数定义：函数 \( f(x) \) 在点 \( x_0 \) 处的导数定义为：
                    \[ f'(x_0) = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x} \]
                </div>
                <div class="math-formula">
                    基本导数公式：
                    <ul>
                        <li>\( (x^n)' = nx^{n-1} \)</li>
                        <li>\( (\sin x)' = \cos x \)</li>
                        <li>\( (e^x)' = e^x \)</li>
                        <li>\( (\ln x)' = \frac{1}{x} \)</li>
                    </ul>
                </div>
                如果您有具体问题，可以进一步描述，我会为您详细解答。`;
            } else if (message.includes('积分')) {
                response = `关于积分的问题，以下是一些基本概念：
                <div class="math-formula">
                    不定积分：若 \( F'(x) = f(x) \)，则 \( \int f(x) \, dx = F(x) + C \)
                </div>
                <div class="math-formula">
                    定积分：\( \int_a^b f(x) \, dx = F(b) - F(a) \)
                </div>
                <div class="math-formula">
                    常见积分公式：
                    <ul>
                        <li>\( \int x^n \, dx = \frac{x^{n+1}}{n+1} + C \) (n ≠ -1)</li>
                        <li>\( \int \frac{1}{x} \, dx = \ln|x| + C \)</li>
                        <li>\( \int e^x \, dx = e^x + C \)</li>
                        <li>\( \int \cos x \, dx = \sin x + C \)</li>
                    </ul>
                </div>`;
            } else if (message.includes('练习题') || message.includes('题目')) {
                response = `好的，以下是5道高等数学练习题：
                <div class="math-formula">
                    1. 求函数 \( f(x) = x^3 - 3x^2 + 2 \) 的极值点和拐点。
                </div>
                <div class="math-formula">
                    2. 计算积分：\( \int_0^{\pi/2} \sin^3 x \, dx \)
                </div>
                <div class="math-formula">
                    3. 求微分方程 \( y'' - 4y' + 4y = e^{2x} \) 的通解。
                </div>
                <div class="math-formula">
                    4. 设向量 \( \vec{a} = (1, 2, 3) \), \( \vec{b} = (2, -1, 0) \)，求 \( \vec{a} \times \vec{b} \)。
                </div>
                <div class="math-formula">
                    5. 求曲面 \( z = x^2 + y^2 \) 在点 (1, 1, 2) 处的切平面方程。
                </div>`;
            } else if (message.includes('帮助') || message.includes('功能')) {
                response = `我是高数帮AI助手，可以为您提供以下帮助：
                <div class="math-formula">
                    <strong>主要功能：</strong>
                    <ul>
                        <li>解答高等数学问题（微积分、线性代数、概率统计等）</li>
                        <li>生成练习题和模拟试卷</li>
                        <li>提供分步解题过程和答案解析</li>
                        <li>分析学习进度和薄弱环节</li>
                        <li>批改作业和试卷</li>
                    </ul>
                </div>
                <div class="math-formula">
                    <strong>使用示例：</strong>
                    <ul>
                        <li>"解释洛必达法则"</li>
                        <li>"求函数 f(x)=x^2+2x 的导数"</li>
                        <li>"生成3道定积分练习题"</li>
                        <li>"帮我分析最近的学习情况"</li>
                    </ul>
                </div>`;
            } else {
                response = `我已收到您的查询："${message}"。作为高数帮AI，我可以：
                <ul>
                    <li>解答高等数学问题</li>
                    <li>生成练习题和试卷</li>
                    <li>分析学习进度和薄弱点</li>
                    <li>提供分步解题过程</li>
                    <li>解释数学概念和定理</li>
                </ul>
                请具体描述您的问题，我会尽力为您提供帮助。`;
            }
            
            addMessage(response, 'ai');
        }, 1500 + Math.random() * 1000);
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