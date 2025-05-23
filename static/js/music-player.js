window.audio = document.getElementById('bgm-player');
window.playlist = []; // 初始化为空数组
const playBtn = document.getElementById('playBtn');
let currentTrack = 0;
let playMode = localStorage.getItem('playMode') || 'list';

// 在initPlayer函数中添加获取逻辑
function initPlayer() {
    // 新增获取播放列表逻辑
    fetch('/api/music-list/')
        .then(response => response.json())
        .then(data => {
            window.playlist = data;
            const savedState = localStorage.getItem('playerState');
            
            if (savedState) {
                const state = JSON.parse(savedState);
                currentTrack = state.currentTrack % data.length;
                audio.src = playlist[currentTrack];
                
                // 确保元数据加载完成后再恢复状态
                audio.onloadedmetadata = () => {
                    audio.currentTime = state.currentTime;
                    if (state.isPlaying) {
                        audio.play().catch(e => {
                            console.log('自动播放被阻止');
                            audio.currentTime = 0; // 阻止后重置进度
                            savePlayerState();
                        });
                    }
                };
                audio.load();
            }
        })
        .catch(error => console.error('获取音乐列表失败:', error));

    // 初始化音频源
    window.audio.src = window.playlist[currentTrack];
    audio.load();
    audio.loop = playMode === 'single';
    document.getElementById('playMode').value = playMode;

    // 事件绑定
    document.addEventListener('visibilitychange', handleVisibilityChange);
    playBtn.addEventListener('click', togglePlay);
    audio.addEventListener('play', () => playBtn.textContent = '⏸️');
    audio.addEventListener('pause', () => playBtn.textContent = '▶️');
    audio.addEventListener('timeupdate', updateProgress);
    audio.addEventListener('ended', handleTrackEnd);
    audio.addEventListener('play', savePlayerState);
    audio.addEventListener('pause', savePlayerState);
    audio.addEventListener('seeked', savePlayerState);

    // 状态恢复逻辑
    const savedState = localStorage.getItem('playerState');
    if (savedState) {
        const state = JSON.parse(savedState);
        currentTrack = state.currentTrack || 0;
        // 修改为异步加载
        audio.onloadedmetadata = () => {
            audio.currentTime = 0;
            if (state.isPlaying) {
                audio.play().catch(e => {
                    console.log('自动播放被阻止');
                    savePlayerState();
                });
            }
        };
    }
    updateSongInfo();
}

function handleVisibilityChange() {
    if (document.hidden) {
        savePlayerState();
        if (!audio.paused) audio.pause();
    } else {
        const savedState = localStorage.getItem('playerState');
        if (savedState) {
            const newState = JSON.parse(savedState);
            // 强制重新加载音频源
            audio.src = playlist[newState.currentTrack];
            audio.load();
            audio.onloadedmetadata = () => {
                audio.currentTime = newState.currentTime;
                if (newState.isPlaying) {
                    setTimeout(() => audio.play(), 300);
                }
            };
        }
    }
}

function togglePlay() {
    if (audio.paused) {
        const restoreState = () => {
            const state = JSON.parse(localStorage.getItem('playerState'));
            audio.currentTime = state?.currentTime || 0;
            audio.play()
                .then(() => savePlayerState())
                .catch(error => {
                    console.error('播放失败:', error);
                    savePlayerState();
                });
        };

        if (audio.src !== playlist[currentTrack]) {
            audio.src = playlist[currentTrack];
            audio.load();
            audio.addEventListener('canplay', restoreState, { once: true });
        } else {
            restoreState();
        }
    } else {
        audio.pause();
        savePlayerState();
    }
}

function savePlayerState() {
    const state = {
        currentTrack: currentTrack,
        currentTime: audio.currentTime,
        isPlaying: !audio.paused,
        timestamp: Date.now()  // 新增时间戳
    };
    localStorage.setItem('playerState', JSON.stringify(state));
}

function updateProgress() {
    const progress = (audio.currentTime / audio.duration) * 100 || 0;
    document.querySelector('.progress-bar').style.width = `${progress}%`;
    // 移除单独的audioTime存储
}

function handleTrackEnd() {
    if(playMode === 'random') {
        currentTrack = Math.floor(Math.random() * playlist.length);
    } else if(playMode === 'list') {
        currentTrack = (currentTrack + 1) % playlist.length;
    }
    
    // 新增防抖处理
    const playPromise = audio.play().catch(e => {
        console.log('自动播放失败:', e);
        savePlayerState();
    });
    
    if(playPromise !== undefined) {
        playPromise.then(() => {
            audio.src = playlist[currentTrack];
            savePlayerState();
        }).catch(e => console.log('播放中断处理:', e));
    }
}

function togglePlayer() {
    const player = document.querySelector('.music-player');
    player.classList.toggle('expanded');
}

function updateSongInfo() {
    const songName = window.playlist[currentTrack].split('/').pop().replace('.mp3', '');
    document.getElementById('songInfo').textContent = songName;
}

// 在skipNext和skipPrevious函数中添加
function skipNext() {
    currentTrack = (currentTrack + 1) % playlist.length;
    audio.src = playlist[currentTrack];
    audio.currentTime = 0;  // 强制重置进度
    savePlayerState();  // 立即保存新状态
    updateProgress();
    audio.play()
        .then(() => updateSongInfo())
        .catch(e => console.error('切歌失败:', e));
}

function skipPrevious() {
    currentTrack = (currentTrack - 1 + playlist.length) % playlist.length;
    audio.src = playlist[currentTrack];
    audio.currentTime = 0;  // 强制重置进度
    savePlayerState();  // 立即保存新状态
    updateProgress();
    audio.play()
        .then(() => updateSongInfo())
        .catch(e => console.error('切歌失败:', e));
}

// 修正歌曲结束处理逻辑
function handleTrackEnd() {
    if(playMode === 'random') {
        currentTrack = Math.floor(Math.random() * playlist.length);
    } else if(playMode === 'list') {
        currentTrack = (currentTrack + 1) % playlist.length;
    }
    
    audio.src = playlist[currentTrack];
    audio.currentTime = 0;  // 新增重置进度
    savePlayerState();  // 新增保存状态
    audio.play().catch(e => console.log('自动播放失败:', e));
}

// 事件绑定
document.addEventListener('DOMContentLoaded', initPlayer);
window.addEventListener('beforeunload', savePlayerState);
document.getElementById('playMode').addEventListener('change', (e) => {
    playMode = e.target.value;
    localStorage.setItem('playMode', playMode);
    audio.loop = playMode === 'single';
});

// 全局访问
window.togglePlay = togglePlay;
window.skipNext = skipNext;
window.skipPrevious = skipPrevious;
// 在初始化事件绑定区域添加
audio.addEventListener('loadeddata', () => {
    updateProgress();
});