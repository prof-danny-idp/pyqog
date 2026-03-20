/**
 * Language switcher for pyqog documentation site.
 * Handles PT-BR / EN language toggling with localStorage persistence.
 */

(function () {
    'use strict';

    const STORAGE_KEY = 'pyqog_lang';

    /**
     * Get the current language from the page path.
     * Returns 'pt' or 'en', or null if on the root landing page.
     */
    function getCurrentLang() {
        const path = window.location.pathname;
        if (path.includes('/pt/')) return 'pt';
        if (path.includes('/en/')) return 'en';
        return null;
    }

    /**
     * Get the equivalent page path in the other language.
     */
    function getSwitchedPath(targetLang) {
        const path = window.location.pathname;
        const currentLang = getCurrentLang();

        if (!currentLang) {
            // On root landing page, go to the target language index
            return targetLang + '/index.html';
        }

        if (currentLang === 'pt' && targetLang === 'en') {
            return path
                .replace('/pt/', '/en/')
                .replace('instalacao.html', 'installation.html');
        }

        if (currentLang === 'en' && targetLang === 'pt') {
            return path
                .replace('/en/', '/pt/')
                .replace('installation.html', 'instalacao.html');
        }

        return path;
    }

    /**
     * Save language preference to localStorage.
     */
    function saveLangPreference(lang) {
        try {
            localStorage.setItem(STORAGE_KEY, lang);
        } catch (e) {
            // localStorage not available, silently ignore
        }
    }

    /**
     * Get saved language preference.
     */
    function getSavedLang() {
        try {
            return localStorage.getItem(STORAGE_KEY);
        } catch (e) {
            return null;
        }
    }

    /**
     * Update active state on language buttons.
     */
    function updateButtons() {
        const currentLang = getCurrentLang();
        document.querySelectorAll('.btn-lang').forEach(function (btn) {
            const btnLang = btn.getAttribute('data-lang');
            if (btnLang === currentLang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    /**
     * Initialize language switcher buttons.
     */
    function initSwitcher() {
        document.querySelectorAll('.btn-lang').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                var targetLang = this.getAttribute('data-lang');
                saveLangPreference(targetLang);
                var newPath = getSwitchedPath(targetLang);
                window.location.href = newPath;
            });
        });
        updateButtons();
    }

    /**
     * On the root landing page, redirect to saved language if available.
     */
    function checkRedirect() {
        if (!getCurrentLang()) {
            var saved = getSavedLang();
            if (saved && (saved === 'pt' || saved === 'en')) {
                // On root page with a saved preference — redirect
                window.location.href = saved + '/index.html';
            }
        }
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initSwitcher();
            checkRedirect();
        });
    } else {
        initSwitcher();
        checkRedirect();
    }
})();
