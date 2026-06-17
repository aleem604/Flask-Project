// ============================================
// DASHBOARD JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ============================================
    // CHARTS INITIALIZATION
    // ============================================
    
    // Colors
    const colors = {
        primary: '#667eea',
        secondary: '#764ba2',
        success: '#2ecc71',
        danger: '#ff4757',
        warning: '#f39c12',
        info: '#3498db',
        purple: '#a29bfe',
        orange: '#f0932b',
        pink: '#ff6b6b',
        teal: '#00b894'
    };

    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart');
    if (revenueCtx) {
        const revenueChart = new Chart(revenueCtx, {
            type: 'line',
            data: {
                labels: dashboardData.revenueData.labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Revenue',
                    data: dashboardData.revenueData.values || [1200, 1900, 1500, 2200, 2800, 2500, 3200],
                    borderColor: colors.primary,
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: colors.primary,
                    pointBorderColor: 'white',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });

        // Update chart on period change
        document.getElementById('revenuePeriod').addEventListener('change', function() {
            const period = this.value;
            // Fetch new data from server
            fetch(`/api/dashboard/revenue?period=${period}`)
                .then(response => response.json())
                .then(data => {
                    revenueChart.data.labels = data.labels;
                    revenueChart.data.datasets[0].data = data.values;
                    revenueChart.update();
                    showToast('Revenue chart updated!', 'info');
                })
                .catch(() => {
                    showToast('Error loading revenue data', 'error');
                });
        });
    }

    // Orders Chart
    const ordersCtx = document.getElementById('ordersChart');
    if (ordersCtx) {
        const ordersChart = new Chart(ordersCtx, {
            type: 'bar',
            data: {
                labels: dashboardData.ordersData.labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Orders',
                    data: dashboardData.ordersData.values || [12, 19, 15, 22, 28, 20, 30],
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.7)',
                        'rgba(118, 75, 162, 0.7)',
                        'rgba(46, 204, 113, 0.7)',
                        'rgba(243, 156, 18, 0.7)',
                        'rgba(255, 71, 87, 0.7)',
                        'rgba(52, 152, 219, 0.7)',
                        'rgba(162, 155, 254, 0.7)'
                    ],
                    borderColor: [
                        '#667eea',
                        '#764ba2',
                        '#2ecc71',
                        '#f39c12',
                        '#ff4757',
                        '#3498db',
                        '#a29bfe'
                    ],
                    borderWidth: 2,
                    borderRadius: 8,
                    barPercentage: 0.7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' orders';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 5
                        }
                    }
                }
            }
        });

        // Update chart on period change
        document.getElementById('ordersPeriod').addEventListener('change', function() {
            const period = this.value;
            fetch(`/api/dashboard/orders?period=${period}`)
                .then(response => response.json())
                .then(data => {
                    ordersChart.data.labels = data.labels;
                    ordersChart.data.datasets[0].data = data.values;
                    ordersChart.update();
                    showToast('Orders chart updated!', 'info');
                })
                .catch(() => {
                    showToast('Error loading orders data', 'error');
                });
        });
    }

    // ============================================
    // ANIMATE STATS NUMBERS
    // ============================================
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const text = stat.textContent;
        const isCurrency = text.includes('$');
        const isPercentage = text.includes('%');
        
        // Remove currency/percentage symbols for animation
        const targetValue = parseFloat(text.replace(/[$,%]/g, ''));
        
        if (!isNaN(targetValue) && targetValue > 0) {
            let currentValue = 0;
            const duration = 2000;
            const steps = 60;
            const increment = targetValue / steps;
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= targetValue) {
                    currentValue = targetValue;
                    clearInterval(timer);
                }
                
                if (isCurrency) {
                    stat.textContent = '$' + currentValue.toFixed(2);
                } else if (isPercentage) {
                    stat.textContent = currentValue.toFixed(1) + '%';
                } else {
                    stat.textContent = Math.round(currentValue);
                }
            }, duration / steps);
        }
    });

    // ============================================
    // CATEGORY BAR ANIMATION
    // ============================================
    const categoryBars = document.querySelectorAll('.category-bar');
    
    const barObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
                barObserver.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    
    categoryBars.forEach(bar => {
        barObserver.observe(bar);
    });

    // ============================================
    // QUICK ACTIONS
    // ============================================
    const quickActions = document.querySelectorAll('.quick-action');
    
    quickActions.forEach(action => {
        action.addEventListener('click', function(e) {
            e.preventDefault();
            const text = this.querySelector('span').textContent;
            showToast(`Navigating to ${text}...`, 'info');
            
            setTimeout(() => {
                // Simulate navigation
                // window.location.href = this.href;
            }, 1000);
        });
    });

    // ============================================
    // ACTIVITY REFRESH
    // ============================================
    const viewAllLinks = document.querySelectorAll('.view-all');
    
    viewAllLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            showToast('Loading more activities...', 'info');
        });
    });

    // ============================================
    // TOAST NOTIFICATION
    // ============================================
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');
    let toastTimeout;

    function showToast(message, type = 'success') {
        toastMessage.textContent = message;
        toast.className = 'toast';
        toast.classList.add(type);
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-times-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        toastIcon.className = icons[type] || icons.success;
        toast.classList.add('show');
        
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    // ============================================
    // KEYBOARD SHORTCUTS
    // ============================================
    document.addEventListener('keydown', function(e) {
        // Ctrl + R for refresh
        if (e.ctrlKey && e.key === 'r') {
            e.preventDefault();
            showToast('Refreshing dashboard...', 'info');
            setTimeout(() => {
                location.reload();
            }, 500);
        }
        
        // Ctrl + D for dashboard home
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    // ============================================
    // REAL-TIME UPDATES (Simulated)
    // ============================================
    // Check for new data every 30 seconds
    setInterval(() => {
        // Only if page is visible
        if (!document.hidden) {
            // Simulate real-time update
            // In production, you would fetch new data
            console.log('Checking for updates...');
        }
    }, 30000);

    // ============================================
    // PRINT DASHBOARD
    // ============================================
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'p') {
            // Allow normal print behavior
        }
    });

    console.log('📊 Dashboard initialized successfully!');
});