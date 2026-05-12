/**
 * IP Countdown Timer JavaScript
 * Handles client-side countdown display and AJAX communication
 */

function initIPCountdown(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Support both old and new formats
    const minutesSpan = element.querySelector('.minutes');
    const secondsSpan = element.querySelector('.seconds');
    const statusDiv = element.querySelector('.countdown-status');

    let countdownInterval;
    let remainingTime = 0;

    // Initialize the timer
    function initTimer() {
        jQuery.ajax({
            url: ip_countdown_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'get_timer_data',
                nonce: ip_countdown_ajax.nonce
            },
            success: function (response) {
                if (response.success) {
                    remainingTime = response.data.remaining_time;

                    if (response.data.is_expired) {
                        showTimerExpired();
                    } else if (remainingTime > 0) {
                        startCountdown();
                        // Remove status messages for inline display
                        if (statusDiv) {
                            statusDiv.style.display = 'none';
                        }
                    } else {
                        showTimerExpired();
                    }
                }
                // Remove error handling messages
            },
            error: function () {
                // Silent error handling
                showTimerExpired();
            }
        });
    }

    // Start the countdown display
    function startCountdown() {
        if (countdownInterval) {
            clearInterval(countdownInterval);
        }

        updateDisplay();

        countdownInterval = setInterval(function () {
            remainingTime--;

            if (remainingTime <= 0) {
                clearInterval(countdownInterval);
                showTimerExpired();
                return;
            }

            updateDisplay();
        }, 1000);
    }

    // Update the timer display
    function updateDisplay() {
        const hours = Math.floor(remainingTime / 3600);
        const minutes = Math.floor((remainingTime % 3600) / 60);
        const seconds = remainingTime % 60;

        const hoursStr = hours.toString().padStart(2, '0');
        const minutesStr = minutes.toString().padStart(2, '0');
        const secondsStr = seconds.toString().padStart(2, '0');

        // Check if we have the new card format with individual digit spans
        const hoursTens = element.querySelector('.hours-tens');
        const hoursOnes = element.querySelector('.hours-ones');
        const minutesTens = element.querySelector('.minutes-tens');
        const minutesOnes = element.querySelector('.minutes-ones');
        const secondsTens = element.querySelector('.seconds-tens');
        const secondsOnes = element.querySelector('.seconds-ones');

        if (minutesTens && minutesOnes && secondsTens && secondsOnes) {
            // New card format - individual digits

            // Update hours if they exist
            if (hoursTens && hoursOnes) {
                updateDigitWithAnimation(hoursTens, hoursStr[0]);
                updateDigitWithAnimation(hoursOnes, hoursStr[1]);
            }

            updateDigitWithAnimation(minutesTens, minutesStr[0]);
            updateDigitWithAnimation(minutesOnes, minutesStr[1]);
            updateDigitWithAnimation(secondsTens, secondsStr[0]);
            updateDigitWithAnimation(secondsOnes, secondsStr[1]);
        } else if (minutesSpan && secondsSpan) {
            // Legacy format - full minutes and seconds
            minutesSpan.textContent = minutesStr;
            secondsSpan.textContent = secondsStr;
        }
    }

    // Show expired state
    function showTimerExpired() {
        // Check if we have the new card format with individual digit spans
        const hoursTens = element.querySelector('.hours-tens');
        const hoursOnes = element.querySelector('.hours-ones');
        const minutesTens = element.querySelector('.minutes-tens');
        const minutesOnes = element.querySelector('.minutes-ones');
        const secondsTens = element.querySelector('.seconds-tens');
        const secondsOnes = element.querySelector('.seconds-ones');

        if (minutesTens && minutesOnes && secondsTens && secondsOnes) {
            // New card format - individual digits

            // Reset hours if they exist
            if (hoursTens && hoursOnes) {
                hoursTens.textContent = '0';
                hoursOnes.textContent = '0';
            }

            minutesTens.textContent = '0';
            minutesOnes.textContent = '0';
            secondsTens.textContent = '0';
            secondsOnes.textContent = '0';
        } else if (minutesSpan && secondsSpan) {
            // Legacy format - full minutes and seconds
            minutesSpan.textContent = '00';
            secondsSpan.textContent = '00';
        }

        // Remove status messages and just add expired class
        if (statusDiv) {
            statusDiv.style.display = 'none';
        }
        element.classList.add('expired');

        if (countdownInterval) {
            clearInterval(countdownInterval);
        }
    }

    // Handle page visibility changes
    document.addEventListener('visibilitychange', function () {
        if (!document.hidden && remainingTime > 0) {
            // Page became visible again - sync with server
            initTimer();
        }
    });

    // Handle page focus
    window.addEventListener('focus', function () {
        if (remainingTime > 0) {
            // Page gained focus - sync with server
            initTimer();
        }
    });

    // Start the timer
    initTimer();
}

// Utility function to format time
function formatTime(seconds, showHours = false) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    if (showHours) {
        return hours.toString().padStart(2, '0') + ':' +
            minutes.toString().padStart(2, '0') + ':' +
            remainingSeconds.toString().padStart(2, '0');
    } else {
        return minutes.toString().padStart(2, '0') + ':' +
            remainingSeconds.toString().padStart(2, '0');
    }
}

// Function to update digit with animation
function updateDigitWithAnimation(digitElement, newValue) {
    // Only animate if value actually changed
    if (digitElement.textContent !== newValue) {
        // Get animation type from the container class
        const container = digitElement.closest('.countdown-cards');
        let animationType = 'none';

        if (container) {
            const classList = container.classList;
            for (let className of classList) {
                if (className.startsWith('ip-countdown-')) {
                    animationType = className.replace('ip-countdown-', '');
                    break;
                }
            }
        }

        // Apply animation based on type
        switch (animationType) {
            case 'flip':
                digitElement.classList.add('flipping');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('flipping');
                }, 300);
                break;

            case 'slide':
                digitElement.classList.add('sliding');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('sliding');
                }, 250);
                break;

            case 'scale':
                digitElement.classList.add('scaling');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('scaling');
                }, 200);
                break;

            case 'bounce':
                digitElement.classList.add('bouncing');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('bouncing');
                }, 300);
                break;

            case 'fade':
                digitElement.classList.add('fading');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('fading');
                }, 250);
                break;

            case 'rotate':
                digitElement.classList.add('rotating');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('rotating');
                }, 250);
                break;

            case 'pulse':
                digitElement.classList.add('pulsing');
                setTimeout(() => {
                    digitElement.textContent = newValue;
                    digitElement.classList.remove('pulsing');
                }, 300);
                break;

            default:
                // No animation, just update immediately
                digitElement.textContent = newValue;
                break;
        }
    }
}