/* ==========================================================================
   مفروشات الشهباء / AL-SHAHBA LUXURY FURNITURE
   MAIN INTERACTIVE SCRIPT (GSAP + ScrollTrigger + Lenis + i18n + Theme Switch)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // Register GSAP Plugins
    gsap.registerPlugin(ScrollTrigger, Flip);

    // Dynamic Year in Footer
    const yearElem = document.getElementById("year");
    if (yearElem) yearElem.textContent = new Date().getFullYear();

    /* ----------------------------------------------------------------------
       1. LENIS SMOOTH SCROLL INTEGRATION
       ---------------------------------------------------------------------- */
    let lenis;
    try {
        lenis = new Lenis({
            duration: 1.2,
            easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
            orientation: 'vertical',
            gestureOrientation: 'vertical',
            smoothWheel: true,
            wheelMultiplier: 1,
            touchMultiplier: 1.5,
        });

        lenis.on('scroll', ScrollTrigger.update);

        gsap.ticker.add((time) => {
            lenis.raf(time * 1000);
        });

        gsap.ticker.lagSmoothing(0);
    } catch (e) {
        console.warn("Lenis initialization skipped or fallback used:", e);
    }

    /* ----------------------------------------------------------------------
       2. BILINGUAL SUPPORT (AR / EN)
       ---------------------------------------------------------------------- */
    const langToggleBtn = document.getElementById("lang-toggle");
    let currentLang = "ar";

    function setLanguage(lang) {
        currentLang = lang;
        const html = document.documentElement;

        if (lang === "en") {
            html.setAttribute("lang", "en");
            html.setAttribute("dir", "ltr");
            if (langToggleBtn) {
                langToggleBtn.querySelector(".lang-text").textContent = "العربية";
            }
        } else {
            html.setAttribute("lang", "ar");
            html.setAttribute("dir", "rtl");
            if (langToggleBtn) {
                langToggleBtn.querySelector(".lang-text").textContent = "EN";
            }
        }

        // Update all elements with data-ar and data-en
        document.querySelectorAll("[data-ar]").forEach((elem) => {
            const text = elem.getAttribute(`data-${lang}`);
            if (text) {
                if (elem.tagName === "INPUT" || elem.tagName === "TEXTAREA") {
                    elem.placeholder = text;
                } else {
                    elem.textContent = text;
                }
            }
        });

        // Refresh GSAP ScrollTrigger to recalculate directions/positions
        setTimeout(() => {
            ScrollTrigger.refresh();
        }, 100);
    }

    if (langToggleBtn) {
        langToggleBtn.addEventListener("click", () => {
            const nextLang = currentLang === "ar" ? "en" : "ar";
            setLanguage(nextLang);
        });
    }

    /* ----------------------------------------------------------------------
       3. DARK / LIGHT THEME TOGGLE (SOCKET SWITCH)
       ---------------------------------------------------------------------- */
    const themeToggleBtn = document.getElementById("theme-toggle");

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("alshahba_theme", theme);
    }

    // Load saved or default theme
    const savedTheme = localStorage.getItem("alshahba_theme") || "dark";
    setTheme(savedTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            const currentTheme = document.documentElement.getAttribute("data-theme") || "dark";
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            setTheme(newTheme);
        });

        themeToggleBtn.addEventListener("keydown", (e) => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                themeToggleBtn.click();
            }
        });
    }

    /* ----------------------------------------------------------------------
       4. 3D MODEL STORYTELLING SEQUENCE
       ---------------------------------------------------------------------- */
    const storyModel = document.getElementById("story-model");
    const storyModelWrapper = document.getElementById("story-model-wrapper");
    const storySection = document.getElementById("story-section");
    const badgeStepNum = document.getElementById("badge-step-num");
    const badgeStepText = document.getElementById("badge-step-text");

    const stepInfo = [
        { num: "01 / 06", ar: "إرث الأصالة الدمشقية", en: "Damascene Heritage Legacy" },
        { num: "02 / 06", ar: "النحت اليدوي والأربيسك", en: "Hand-Carved Arabesque Art" },
        { num: "03 / 06", ar: "التطعيم بالصدف والتذهيب", en: "Inlaid Mother-of-Pearl & Gold" },
        { num: "04 / 06", ar: "الحرير المخملي والراحة الأبدية", en: "Royal Silk Velvet Cushioning" },
        { num: "05 / 06", ar: "الهندسة المريحة المتكاملة", en: "Precision Ergonomic Contour" },
        { num: "06 / 06", ar: "اللمسات النهائية الشاملة", en: "Master Artisan Polish" }
    ];

    if (storySection && storyModelWrapper) {
        // Create ScrollTrigger timeline for 3D chair gliding & rotating
        const storyTL = gsap.timeline({
            scrollTrigger: {
                trigger: storySection,
                start: "top top",
                end: "bottom bottom",
                scrub: 1,
            }
        });

        // Alternating positions & rotations
        storyTL
            .to(storyModelWrapper, { xPercent: -28, duration: 1 })
            .to(storyModelWrapper, { xPercent: 28, duration: 1 })
            .to(storyModelWrapper, { xPercent: -22, duration: 1 })
            .to(storyModelWrapper, { xPercent: 22, duration: 1 })
            .to(storyModelWrapper, { xPercent: 0, duration: 1 });

        // Update 3D Camera Orbit on scroll
        ScrollTrigger.create({
            trigger: storySection,
            start: "top top",
            end: "bottom bottom",
            onUpdate: (self) => {
                const p = self.progress;
                const angle = Math.floor(p * 360 * 2); // 2 full rotations over story
                if (storyModel) {
                    storyModel.setAttribute("camera-orbit", `${angle}deg 75deg 2.5m`);
                }

                // Update floating step badge
                const stepIdx = Math.min(Math.floor(p * 6), 5);
                if (badgeStepNum && badgeStepText) {
                    badgeStepNum.textContent = stepInfo[stepIdx].num;
                    const label = currentLang === "ar" ? stepInfo[stepIdx].ar : stepInfo[stepIdx].en;
                    badgeStepText.textContent = label;
                }
            }
        });

        // Animate story step cards fade & slide in
        gsap.utils.toArray(".story-step").forEach((step, i) => {
            const card = step.querySelector(".step-card");
            if (card) {
                gsap.from(card, {
                    scrollTrigger: {
                        trigger: step,
                        start: "top 75%",
                        end: "top 35%",
                        scrub: 0.5,
                    },
                    opacity: 0,
                    y: 60,
                    scale: 0.9,
                });
            }
        });
    }

    /* ----------------------------------------------------------------------
       5. 3D MODEL DOCKING INTO PRODUCT CARD 5
       ---------------------------------------------------------------------- */
    const dockSlot = document.getElementById("dock-card-slot");
    const dockTarget = document.getElementById("dock-target");

    if (dockSlot && dockTarget && storyModelWrapper && storyModel) {
        ScrollTrigger.create({
            trigger: dockSlot,
            start: "top 60%",
            end: "top 20%",
            scrub: 0.8,
            onEnter: () => {
                // Dock model into Card 5 container
                dockTarget.appendChild(storyModelWrapper);
                storyModelWrapper.style.position = "relative";
                storyModelWrapper.style.top = "0";
                storyModelWrapper.style.width = "100%";
                storyModelWrapper.style.height = "100%";
                storyModelWrapper.style.transform = "none";

                // Enable interactive camera controls once docked
                storyModel.setAttribute("camera-controls", "true");
                storyModel.setAttribute("touch-action", "pan-y");
                storyModel.setAttribute("auto-rotate", "true");

                // Hide placeholder overlay
                const overlay = document.getElementById("dock-placeholder-overlay");
                if (overlay) overlay.style.opacity = "0";
            },
            onLeaveBack: () => {
                // Undock back to story section
                const storyViewport = document.getElementById("story-pinned-viewport");
                if (storyViewport) {
                    storyViewport.appendChild(storyModelWrapper);
                    storyModelWrapper.style.position = "sticky";
                    storyModelWrapper.style.top = "15vh";
                    storyModelWrapper.style.width = "500px";
                    storyModelWrapper.style.height = "500px";

                    storyModel.removeAttribute("camera-controls");
                    storyModel.removeAttribute("touch-action");
                    storyModel.removeAttribute("auto-rotate");

                    const overlay = document.getElementById("dock-placeholder-overlay");
                    if (overlay) overlay.style.opacity = "1";
                }
            }
        });
    }

    /* ----------------------------------------------------------------------
       6. CANVAS 60-FRAME SCRUBBING
       ---------------------------------------------------------------------- */
    const canvas = document.getElementById("frame-canvas");
    const frameScrubSection = document.getElementById("craft-section");
    const frameScrubPinned = document.getElementById("frame-scrub-pinned");
    const scrubProgressFill = document.getElementById("scrub-progress-fill");
    const scrubCounter = document.getElementById("scrub-counter");

    if (canvas && frameScrubSection && frameScrubPinned) {
        const ctx = canvas.getContext("2d");
        const frameCount = 60;
        const images = [];
        const airbnbFrame = { current: 0 };

        // Preload frame images
        let loadedImages = 0;

        for (let i = 1; i <= frameCount; i++) {
            const img = new Image();
            const padNum = String(i).padStart(3, "0");
            img.src = `assets/frames/frame_${padNum}.jpg`;
            img.onload = () => {
                loadedImages++;
                if (i === 1) {
                    renderFrame(0);
                }
            };
            images.push(img);
        }

        function renderFrame(index) {
            const img = images[index];
            if (img && img.complete) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            }
        }

        // ScrollTrigger frame scrubbing timeline
        gsap.to(airbnbFrame, {
            current: frameCount - 1,
            snap: "current",
            ease: "none",
            scrollTrigger: {
                trigger: frameScrubSection,
                start: "top top",
                end: "bottom bottom",
                scrub: 0.3,
                pin: frameScrubPinned,
                onUpdate: (self) => {
                    const frameIdx = Math.round(airbnbFrame.current);
                    renderFrame(frameIdx);

                    // Update progress bar & counter text
                    const progressPct = (self.progress * 100).toFixed(1);
                    if (scrubProgressFill) scrubProgressFill.style.width = `${progressPct}%`;
                    if (scrubCounter) {
                        const numStr = String(frameIdx + 1).padStart(2, "0");
                        scrubCounter.textContent = `FRAME ${numStr} / 60`;
                    }

                    // Annotations visibility based on scrub progress
                    const a1 = document.getElementById("annot-1");
                    const a2 = document.getElementById("annot-2");
                    const a3 = document.getElementById("annot-3");

                    if (a1) a1.classList.toggle("active", self.progress > 0.15 && self.progress < 0.45);
                    if (a2) a2.classList.toggle("active", self.progress >= 0.45 && self.progress < 0.72);
                    if (a3) a3.classList.toggle("active", self.progress >= 0.72 && self.progress < 0.98);
                }
            }
        });
    }
});
