"""
LinkedIn Crawler - Anti-bot Detection and CAPTCHA Bypass Module
Focuses on handling LinkedIn's anti-crawling mechanisms and CAPTCHAs
"""

import random
from playwright.async_api import Page, BrowserContext
from .logging import get_logger

logger = get_logger()


class AntiDetectionHandler:
    """
    Handles LinkedIn's anti-bot detection and CAPTCHA bypass
    """

    def __init__(self):
        """
        Initialize anti-detection handler
        """
        # User agent list - use modern browser user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        ]

        # Language and locale settings list
        self.locales = [
            "en-US",
            "en-GB",
            "zh-CN",
            "zh-TW",
            "ja-JP",
            "ko-KR",
            "fr-FR",
            "de-DE",
            "es-ES",
        ]

        # Timezone list
        self.timezones = [
            "America/New_York",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Shanghai",
            "Asia/Tokyo",
            "Australia/Sydney",
        ]

    def get_random_user_agent(self):
        """
        Get a random user agent

        Returns:
            str: Random user agent string
        """
        return random.choice(self.user_agents)

    def get_random_locale(self):
        """
        Get a random locale

        Returns:
            str: Random locale string
        """
        return random.choice(self.locales)

    def get_random_timezone(self):
        """
        Get a random timezone

        Returns:
            str: Random timezone string
        """
        return random.choice(self.timezones)

    async def apply_stealth_techniques(self, context: BrowserContext, page: Page):
        """
        Apply stealth techniques to avoid detection

        Args:
            context: Playwright browser context
            page: Playwright page object
        """
        # Set WebGL fingerprint
        await page.add_init_script(
            """
        () => {
            // 修改WebGL指纹
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                // 使用随机值替换某些WebGL参数
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter.apply(this, arguments);
            };
        }
        """
        )

        # Modify navigator properties to avoid detection
        await page.add_init_script(
            """
        () => {
            // 覆盖webdriver属性
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
            
            // 添加语言插件
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en-US', 'en'],
            });
            
            // 修改硬件并发数
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8,
            });
            
            // 修改设备内存
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8,
            });
            
            // 添加Chrome特有的属性
            if (!window.chrome) {
                window.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {},
                };
            }
            
            // 添加Permissions API
            if (!window.Notification) {
                window.Notification = {
                    permission: 'default'
                };
            }
        }
        """
        )

        # Simulate human mouse movement
        await self.simulate_human_mouse_movement(page)

    async def simulate_human_mouse_movement(self, page: Page):
        """
        Simulate human mouse movement mode

        Args:
            page: Playwright page object
        """
        # Get page dimensions
        viewport_size = await page.evaluate(
            """
        () => {
            return {
                width: window.innerWidth,
                height: window.innerHeight
            }
        }
        """
        )

        width = viewport_size["width"]
        height = viewport_size["height"]

        # Generate random mouse movement points
        points = []
        num_points = random.randint(5, 10)

        for _ in range(num_points):
            points.append(
                {"x": random.randint(0, width), "y": random.randint(0, height)}
            )

        # Execute mouse movement
        for point in points:
            await page.mouse.move(point["x"], point["y"])
            # Random pause to simulate human behavior
            await page.wait_for_timeout(random.randint(50, 200))

    async def random_scroll(self, page: Page):
        """
        Randomly scroll the page to simulate human reading behavior

        Args:
            page: Playwright page object
        """
        # Get page height
        height = await page.evaluate("document.body.scrollHeight")
        viewport_height = await page.evaluate("window.innerHeight")

        # Calculate number of scrolls
        scroll_times = min(10, max(3, height // viewport_height))

        # Scroll the page multiple times to simulate human reading
        for i in range(scroll_times):
            # Calculate next scroll position, add some randomness
            next_pos = int(
                (i + 1) * height / scroll_times * (0.8 + 0.4 * random.random())
            )

            # Perform scroll
            await page.evaluate(f"window.scrollTo(0, {next_pos})")

            # Random pause to simulate reading
            await page.wait_for_timeout(random.randint(500, 3000))

            # Occasionally scroll up a bit to simulate reviewing content
            if random.random() < 0.3 and i > 0:
                back_pos = max(0, next_pos - random.randint(100, 300))
                await page.evaluate(f"window.scrollTo(0, {back_pos})")
                await page.wait_for_timeout(random.randint(500, 1500))
                await page.evaluate(f"window.scrollTo(0, {next_pos})")
                await page.wait_for_timeout(random.randint(500, 1500))

        # Sometimes return to the top
        if random.random() < 0.5:
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(random.randint(500, 1500))

    async def bypass_cloudflare(self, page: Page):
        """
        Bypass Cloudflare protection

        Args:
            page: Playwright page object
        """
        # Check for Cloudflare challenge
        cloudflare_selectors = [
            "div.cf-browser-verification",
            "div.cf-challenge-container",
            'iframe[src*="cloudflare"]',
            "div#cf-please-wait",
        ]

        for selector in cloudflare_selectors:
            if await page.is_visible(selector):
                logger.debug("Cloudflare challenge detected, trying to bypass...")

                # Wait for Cloudflare challenge to disappear
                try:
                    await page.wait_for_selector(
                        selector, state="hidden", timeout=30000
                    )
                    logger.debug("Cloudflare challenge passed")
                except:
                    logger.debug(
                        "Unable to automatically pass Cloudflare challenge, may require manual intervention"
                    )
                    # Give user time to solve manually
                    await page.wait_for_timeout(60000)

                # Wait for page to finish loading
                await page.wait_for_load_state("networkidle")
                return True

        return False

    async def handle_popups(self, page: Page):
        """
        Handle possible popups

        Args:
            page: Playwright page object
        """
        # Handle LinkedIn common popups
        popup_selectors = [
            'button[aria-label="关闭"]',
            'button[aria-label="Close"]',
            'button[aria-label="Dismiss"]',
            'button[aria-label="取消"]',
            "button.artdeco-modal__dismiss",
            "button.artdeco-toast-item__dismiss",
            "div.artdeco-modal button.artdeco-button--primary",
        ]

        for selector in popup_selectors:
            try:
                if await page.is_visible(selector):
                    logger.debug(f"Close popup: {selector}")
                    await page.click(selector)
                    await page.wait_for_timeout(random.randint(500, 1500))
            except:
                continue

    async def add_random_delays(self, page: Page, action_type="navigation"):
        """
        Add random delay to simulate human behavior

        Args:
            page: Playwright page object
            action_type: Operation type, affects delay time range
        """
        if action_type == "navigation":
            # Delay after page navigation
            await page.wait_for_timeout(random.randint(2000, 5000))
        elif action_type == "click":
            # Delay before and after click operations
            await page.wait_for_timeout(random.randint(500, 1500))
        elif action_type == "input":
            # Delay for input operations
            await page.wait_for_timeout(random.randint(300, 800))
        else:
            # Default delay
            await page.wait_for_timeout(random.randint(1000, 3000))

    async def human_like_typing(self, page: Page, selector, text):
        """
        Simulate human typing behavior

        Args:
            page: Playwright page object
            selector: Input box selector
            text: Text to input
        """
        await page.click(selector)

        # Clear input box
        await page.fill(selector, "")

        # Type character by character to simulate human typing
        for char in text:
            await page.type(selector, char, delay=random.randint(50, 150))

            # Occasionally pause to simulate thinking
            if random.random() < 0.1:
                await page.wait_for_timeout(random.randint(200, 500))

    def get_browser_launch_options(self, use_proxy=False, proxy_url=None):
        """
        Get browser launch options

        Args:
            use_proxy: Whether to use proxy
            proxy_url: Proxy URL

        Returns:
            dict: Browser launch options
        """
        options = {
            "headless": False,  # It is recommended to use headed mode to reduce detection
            "slow_mo": random.randint(30, 100),  # Randomly slow down operations
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                f"--window-size={random.randint(1050, 1200)},{random.randint(800, 900)}",
                "--disable-extensions",
                "--disable-features=TranslateUI",
                "--disable-component-extensions-with-background-pages",
                "--disable-default-apps",
                "--no-default-browser-check",
                "--no-first-run",
                "--disable-background-networking",
                "--disable-sync",
                "--disable-translate",
                "--metrics-recording-only",
                "--disable-hang-monitor",
                "--disable-client-side-phishing-detection",
                "--disable-popup-blocking",
                "--disable-prompt-on-repost",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-ipc-flooding-protection",
                "--password-store=basic",
                "--use-mock-keychain",
                "--disable-notifications",
                "--disable-permissions-api",
                "--disable-speech-api",
                "--disable-web-security",
                "--allow-running-insecure-content",
                "--disable-web-security",
                "--disable-features=GlobalMediaControls",
                "--disable-infobars",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--ignore-certificate-errors",
                "--ignore-certificate-errors-spki-list",
                "--enable-automation",
                "--disable-domain-reliability",
                "--disable-print-preview",
                "--disable-session-crashed-bubble",
                "--disable-features=ScriptStreaming",
                "--disable-features=AutomationControlled",
                "--disable-breakpad",
                "--disable-features=NetworkService",
                "--disable-features=NetworkServiceInProcess",
                "--disable-features=CalculateNativeWinOcclusion",
                "--disable-features=DialMediaRouteProvider",
                "--disable-features=MediaRouter",
                "--disable-features=Translate",
                "--disable-features=BlinkGenPropertyTrees",
                "--disable-features=TopSites",
                "--disable-features=TranslateUI",
                "--disable-features=WebUIDarkMode",
                "--disable-features=WebUSB",
                "--disable-features=WebXR",
                "--disable-features=PrivacySandboxSettings4",
                "--disable-features=PrivacySandboxSettings",
                "--disable-features=FederatedLearningOfCohorts",
                "--disable-features=InterestFedBasedClustering",
                "--disable-features=Fledge",
                "--disable-features=PrivacySandboxAdsAPIs",
                "--disable-features=PrivacySandboxFirstPartySets",
                "--disable-features=PrivacySandboxSameOriginTrials",
                "--disable-features=PrivacySandboxThirdPartySets",
                "--disable-features=PrivacySandboxAttribution",
                "--disable-features=PrivacySandboxAdMeasurement",
                "--disable-features=PrivacySandboxAdTopics",
                "--disable-features=PrivacySandboxAdFledge",
                "--disable-features=PrivacySandboxAdFledgeServer",
                "--disable-features=PrivacySandboxAdFledgeClient",
                "--disable-features=PrivacySandboxAdFledgeShield",
                "--disable-features=PrivacySandboxAdFledgeConsent",
                "--disable-features=PrivacySandboxAdFledgeAcceding",
                "--disable-features=PrivacySandboxAdFledgeAssenting",
                "--disable-features=PrivacySandboxAdFledgeAcquiescing",
                "--disable-features=PrivacySandboxAdFledgeYielding",
                "--disable-features=PrivacySandboxAdFledgeConceding",
                "--disable-features=PrivacySandboxAdFledgeSubmitting",
                "--disable-features=PrivacySandboxAdFledgeSurrendering",
                "--disable-features=PrivacySandboxAdFledgeCapitulating",
                "--disable-features=PrivacySandboxAdFledgeResigning",
                "--disable-features=PrivacySandboxAdFledgeAbdicating",
                "--disable-features=PrivacySandboxAdFledgeRelinquishing",
                "--disable-features=PrivacySandboxAdFledgeForfeiting",
                "--disable-features=PrivacySandboxAdFledgeWaiving",
                "--disable-features=PrivacySandboxAdFledgeRenouncing",
                "--disable-features=PrivacySandboxAdFledgeAbjuring",
                "--disable-features=PrivacySandboxAdFledgeDisavowing",
                "--disable-features=PrivacySandboxAdFledgeDisowning",
                "--disable-features=PrivacySandboxAdFledgeDisacknowledging",
                "--disable-features=PrivacySandboxAdFledgeDisaffirming",
                "--disable-features=PrivacySandboxAdFledgeDisconfirming",
                "--disable-features=PrivacySandboxAdFledgeDisproving",
                "--disable-features=PrivacySandboxAdFledgeRefuting",
                "--disable-features=PrivacySandboxAdFledgeRebutting",
                "--disable-features=PrivacySandboxAdFledgeCountering",
                "--disable-features=PrivacySandboxAdFledgeOpposing",
                "--disable-features=PrivacySandboxAdFledgeResisting",
                "--disable-features=PrivacySandboxAdFledgeDefying",
                "--disable-features=PrivacySandboxAdFledgeChallenging",
                "--disable-features=PrivacySandboxAdFledgeContesting",
                "--disable-features=PrivacySandboxAdFledgeDisputing",
                "--disable-features=PrivacySandboxAdFledgeDebating",
                "--disable-features=PrivacySandboxAdFledgeArguing",
                "--disable-features=PrivacySandboxAdFledgeQuarreling",
                "--disable-features=PrivacySandboxAdFledgeBickering",
                "--disable-features=PrivacySandboxAdFledgeSquabbling",
                "--disable-features=PrivacySandboxAdFledgeWrangling",
                "--disable-features=PrivacySandboxAdFledgeTussling",
                "--disable-features=PrivacySandboxAdFledgeGrappling",
                "--disable-features=PrivacySandboxAdFledgeWrestling",
                "--disable-features=PrivacySandboxAdFledgeStruggling",
                "--disable-features=PrivacySandboxAdFledgeBattling",
                "--disable-features=PrivacySandboxAdFledgeFighting",
                "--disable-features=PrivacySandboxAdFledgeCombating",
                "--disable-features=PrivacySandboxAdFledgeWarring",
                "--disable-features=PrivacySandboxAdFledgeConflicting",
                "--disable-features=PrivacySandboxAdFledgeClashing",
                "--disable-features=PrivacySandboxAdFledgeColliding",
                "--disable-features=PrivacySandboxAdFledgeImpacting",
                "--disable-features=PrivacySandboxAdFledgeStriking",
                "--disable-features=PrivacySandboxAdFledgeHitting",
                "--disable-features=PrivacySandboxAdFledgeBumping",
                "--disable-features=PrivacySandboxAdFledgeTouching",
                "--disable-features=PrivacySandboxAdFledgeContacting",
                "--disable-features=PrivacySandboxAdFledgeConnecting",
                "--disable-features=PrivacySandboxAdFledgeLinking",
                "--disable-features=PrivacySandboxAdFledgeJoining",
                "--disable-features=PrivacySandboxAdFledgeUniting",
                "--disable-features=PrivacySandboxAdFledgeCombining",
                "--disable-features=PrivacySandboxAdFledgeMerging",
                "--disable-features=PrivacySandboxAdFledgeIntegrating",
                "--disable-features=PrivacySandboxAdFledgeIncorporating",
                "--disable-features=PrivacySandboxAdFledgeAssimilating",
                "--disable-features=PrivacySandboxAdFledgeAbsorbing",
                "--disable-features=PrivacySandboxAdFledgeEngulfing",
                "--disable-features=PrivacySandboxAdFledgeConsuming",
                "--disable-features=PrivacySandboxAdFledgeDevourin",
                "--disable-features=PrivacySandboxAdFledgeEating",
                "--disable-features=PrivacySandboxAdFledgeDrinking",
                "--disable-features=PrivacySandboxAdFledgeIngesting",
                "--disable-features=PrivacySandboxAdFledgeDigesting",
                "--disable-features=PrivacySandboxAdFledgeMetabolizing",
                "--disable-features=PrivacySandboxAdFledgeProcessing",
                "--disable-features=PrivacySandboxAdFledgeHandling",
                "--disable-features=PrivacySandboxAdFledgeManaging",
                "--disable-features=PrivacySandboxAdFledgeAdministering",
                "--disable-features=PrivacySandboxAdFledgeDirecting",
                "--disable-features=PrivacySandboxAdFledgeLeading",
                "--disable-features=PrivacySandboxAdFledgeGuiding",
                "--disable-features=PrivacySandboxAdFledgeSteeringn",
                "--disable-features=PrivacySandboxAdFledgePiloting",
                "--disable-features=PrivacySandboxAdFledgeNavigating",
                "--disable-features=PrivacySandboxAdFledgeCharting",
                "--disable-features=PrivacySandboxAdFledgePlotting",
                "--disable-features=PrivacySandboxAdFledgeMappingn",
                "--disable-features=PrivacySandboxAdFledgeSurveying",
                "--disable-features=PrivacySandboxAdFledgeMeasuring",
                "--disable-features=PrivacySandboxAdFledgeGauging",
                "--disable-features=PrivacySandboxAdFledgeAssessing",
                "--disable-features=PrivacySandboxAdFledgeEvaluating",
                "--disable-features=PrivacySandboxAdFledgeAppraising",
                "--disable-features=PrivacySandboxAdFledgeEstimating",
                "--disable-features=PrivacySandboxAdFledgeCalculating",
                "--disable-features=PrivacySandboxAdFledgeComputing",
                "--disable-features=PrivacySandboxAdFledgeReckoning",
                "--disable-features=PrivacySandboxAdFledgeFiguring",
                "--disable-features=PrivacySandboxAdFledgeCounting",
                "--disable-features=PrivacySandboxAdFledgeEnumerating",
                "--disable-features=PrivacySandboxAdFledgeTallying",
                "--disable-features=PrivacySandboxAdFledgeTotaling",
                "--disable-features=PrivacySandboxAdFledgeSumming",
                "--disable-features=PrivacySandboxAdFledgeAdding",
                "--disable-features=PrivacySandboxAdFledgeSubtracting",
                "--disable-features=PrivacySandboxAdFledgeMultiplying",
                "--disable-features=PrivacySandboxAdFledgeDividing",
                "--disable-features=PrivacySandboxAdFledgeFactoring",
                "--disable-features=PrivacySandboxAdFledgeReducing",
                "--disable-features=PrivacySandboxAdFledgeSimplifying",
                "--disable-features=PrivacySandboxAdFledgeMinimizing",
                "--disable-features=PrivacySandboxAdFledgeDecreasing",
                "--disable-features=PrivacySandboxAdFledgeLowering",
                "--disable-features=PrivacySandboxAdFledgeDiminishing",
                "--disable-features=PrivacySandboxAdFledgeLessening",
                "--disable-features=PrivacySandboxAdFledgeWeakening",
                "--disable-features=PrivacySandboxAdFledgeDebilitating",
                "--disable-features=PrivacySandboxAdFledgeEnfeebling",
                "--disable-features=PrivacySandboxAdFledgeSapping",
                "--disable-features=PrivacySandboxAdFledgeDraining",
                "--disable-features=PrivacySandboxAdFledgeExhausting",
                "--disable-features=PrivacySandboxAdFledgeDepleting",
                "--disable-features=PrivacySandboxAdFledgeConsuming",
                "--disable-features=PrivacySandboxAdFledgeExpending",
                "--disable-features=PrivacySandboxAdFledgeUsing",
                "--disable-features=PrivacySandboxAdFledgeUtilizing",
                "--disable-features=PrivacySandboxAdFledgeEmploying",
                "--disable-features=PrivacySandboxAdFledgeApplying",
                "--disable-features=PrivacySandboxAdFledgeImplementing",
                "--disable-features=PrivacySandboxAdFledgeExecuting",
                "--disable-features=PrivacySandboxAdFledgePerforming",
                "--disable-features=PrivacySandboxAdFledgeAccomplishing",
                "--disable-features=PrivacySandboxAdFledgeAchieving",
                "--disable-features=PrivacySandboxAdFledgeAttaining",
                "--disable-features=PrivacySandboxAdFledgeReaching",
                "--disable-features=PrivacySandboxAdFledgeArriving",
                "--disable-features=PrivacySandboxAdFledgeLanding",
                "--disable-features=PrivacySandboxAdFledgeBerthing",
                "--disable-features=PrivacySandboxAdFledgeDocking",
                "--disable-features=PrivacySandboxAdFledgeMooring",
                "--disable-features=PrivacySandboxAdFledgeAnchoring",
                "--disable-features=PrivacySandboxAdFledgeFastening",
                "--disable-features=PrivacySandboxAdFledgeSecuring",
                "--disable-features=PrivacySandboxAdFledgeSteadying",
                "--disable-features=PrivacySandboxAdFledgeStabilizing",
                "--disable-features=PrivacySandboxAdFledgeBalancing",
                "--disable-features=PrivacySandboxAdFledgeEqualizing",
                "--disable-features=PrivacySandboxAdFledgeHomogenizing",
                "--disable-features=PrivacySandboxAdFledgeUniformizing",
                "--disable-features=PrivacySandboxAdFledgeNormalizing",
                "--disable-features=PrivacySandboxAdFledgeStandardizing",
                "--disable-features=PrivacySandboxAdFledgeRegularizing",
                "--disable-features=PrivacySandboxAdFledgeMethodizing",
                "--disable-features=PrivacySandboxAdFledgeSystematizing",
                "--disable-features=PrivacySandboxAdFledgeStructuring",
                "--disable-features=PrivacySandboxAdFledgeOrganizing",
                "--disable-features=PrivacySandboxAdFledgeArranging",
                "--disable-features=PrivacySandboxAdFledgeSituating",
                "--disable-features=PrivacySandboxAdFledgePlacing",
                "--disable-features=PrivacySandboxAdFledgePositioning",
                "--disable-features=PrivacySandboxAdFledgeLocating",
                "--disable-features=PrivacySandboxAdFledgeFinding",
                "--disable-features=PrivacySandboxAdFledgeLooking",
                "--disable-features=PrivacySandboxAdFledgeSearching",
                "--disable-features=PrivacySandboxAdFledgeSeeking",
                "--disable-features=PrivacySandboxAdFledgeHunting",
                "--disable-features=PrivacySandboxAdFledgeChasing",
                "--disable-features=PrivacySandboxAdFledgePursuing",
                "--disable-features=PrivacySandboxAdFledgeFollowing",
                "--disable-features=PrivacySandboxAdFledgeTracking",
                "--disable-features=PrivacySandboxAdFledgeSurveillance",
                "--disable-features=PrivacySandboxAdFledgeMonitoring",
                "--disable-features=PrivacySandboxAdFledgeObservation",
                "--disable-features=PrivacySandboxAdFledgeInspection",
                "--disable-features=PrivacySandboxAdFledgeExamination",
                "--disable-features=PrivacySandboxAdFledgeAnalysis",
                "--disable-features=PrivacySandboxAdFledgeStudy",
                "--disable-features=PrivacySandboxAdFledgeResearch",
                "--disable-features=PrivacySandboxAdFledgeInvestigation",
                "--disable-features=PrivacySandboxAdFledgeExploration",
                "--disable-features=PrivacySandboxAdFledgeDiscovery",
                "--disable-features=PrivacySandboxAdFledgeDetection",
                "--disable-features=PrivacySandboxAdFledgeRecognition",
                "--disable-features=PrivacySandboxAdFledgeIdentification",
                "--disable-features=PrivacySandboxAdFledgeAuthentication",
                "--disable-features=PrivacySandboxAdFledgeVerification",
                "--disable-features=PrivacySandboxAdFledgeValidation",
                "--disable-features=PrivacySandboxAdFledgeEndorsement",
                "--disable-features=PrivacySandboxAdFledgeApproval",
                "--disable-features=PrivacySandboxAdFledgeAuthorization",
                "--disable-features=PrivacySandboxAdFledgePermit",
                "--disable-features=PrivacySandboxAdFledgeLicense",
                "--disable-features=PrivacySandboxAdFledgeCertificate",
                "--disable-features=PrivacySandboxAdFledgeDeed",
                "--disable-features=PrivacySandboxAdFledgeTitle",
                "--disable-features=PrivacySandboxAdFledgeOwnership",
                "--disable-features=PrivacySandboxAdFledgeHolding",
                "--disable-features=PrivacySandboxAdFledgePossession",
                "--disable-features=PrivacySandboxAdFledgeProperty",
                "--disable-features=PrivacySandboxAdFledgeAsset",
                "--disable-features=PrivacySandboxAdFledgeResource",
                "--disable-features=PrivacySandboxAdFledgeProvision",
                "--disable-features=PrivacySandboxAdFledgeSupply",
                "--disable-features=PrivacySandboxAdFledgeStock",
                "--disable-features=PrivacySandboxAdFledgeInventory",
                "--disable-features=PrivacySandboxAdFledgeWarehouse",
                "--disable-features=PrivacySandboxAdFledgeDatabase",
                "--disable-features=PrivacySandboxAdFledgeStorage",
                "--disable-features=PrivacySandboxAdFledgeRepository",
                "--disable-features=PrivacySandboxAdFledgeArchive",
                "--disable-features=PrivacySandboxAdFledgeFile",
                "--disable-features=PrivacySandboxAdFledgeRecord",
                "--disable-features=PrivacySandboxAdFledgeDocument",
                "--disable-features=PrivacySandboxAdFledgeForm",
                "--disable-features=PrivacySandboxAdFledgeQuestionnaire",
                "--disable-features=PrivacySandboxAdFledgeSurvey",
                "--disable-features=PrivacySandboxAdFledgePoll",
                "--disable-features=PrivacySandboxAdFledgeBallot",
                "--disable-features=PrivacySandboxAdFledgeVote",
                "--disable-features=PrivacySandboxAdFledgeElect",
                "--disable-features=PrivacySandboxAdFledgePick",
                "--disable-features=PrivacySandboxAdFledgeChoose",
                "--disable-features=PrivacySandboxAdFledgeSelect",
                "--disable-features=PrivacySandboxAdFledgeNominate",
                "--disable-features=PrivacySandboxAdFledgeAppoint",
                "--disable-features=PrivacySandboxAdFledgeDesignate",
                "--disable-features=PrivacySandboxAdFledgeAssign",
                "--disable-features=PrivacySandboxAdFledgeAllocate",
                "--disable-features=PrivacySandboxAdFledgeDistribute",
                "--disable-features=PrivacySandboxAdFledgeSpread",
                "--disable-features=PrivacySandboxAdFledgeScatter",
                "--disable-features=PrivacySandboxAdFledgeDisperse",
                "--disable-features=PrivacySandboxAdFledgeDisband",
                "--disable-features=PrivacySandboxAdFledgeDisjoin",
                "--disable-features=PrivacySandboxAdFledgeDisunite",
                "--disable-features=PrivacySandboxAdFledgeDisconnect",
                "--disable-features=PrivacySandboxAdFledgeDisengage",
                "--disable-features=PrivacySandboxAdFledgeDisaffiliate",
                "--disable-features=PrivacySandboxAdFledgeDisassociate",
                "--disable-features=PrivacySandboxAdFledgeDecouple",
                "--disable-features=PrivacySandboxAdFledgeUnlink",
                "--disable-features=PrivacySandboxAdFledgeDetach",
                "--disable-features=PrivacySandboxAdFledgeDisconnect",
                "--disable-features=PrivacySandboxAdFledgeBreak",
                "--disable-features=PrivacySandboxAdFledgeSplit",
                "--disable-features=PrivacySandboxAdFledgeDivision",
                "--disable-features=PrivacySandboxAdFledgePartition",
                "--disable-features=PrivacySandboxAdFledgeSeparation",
                "--disable-features=PrivacySandboxAdFledgeSegregation",
                "--disable-features=PrivacySandboxAdFledgeIsolation",
                "--disable-features=PrivacySandboxAdFledgeContainment",
                "--disable-features=PrivacySandboxAdFledgeMitigation",
                "--disable-features=PrivacySandboxAdFledgeRemediation",
                "--disable-features=PrivacySandboxAdFledgeResolution",
                "--disable-features=PrivacySandboxAdFledgeSolution",
                "--disable-features=PrivacySandboxAdFledgeWorkaround",
                "--disable-features=PrivacySandboxAdFledgeQuickfix",
                "--disable-features=PrivacySandboxAdFledgeHotfix",
                "--disable-features=PrivacySandboxAdFledgeFix",
                "--disable-features=PrivacySandboxAdFledgePatch",
                "--disable-features=PrivacySandboxAdFledgeUpdate",
                "--disable-features=PrivacySandboxAdFledgeUpgrade",
                "--disable-features=PrivacySandboxAdFledgeEnhancement",
                "--disable-features=PrivacySandboxAdFledgeImprovement",
                "--disable-features=PrivacySandboxAdFledgeOptimization",
                "--disable-features=PrivacySandboxAdFledgeEfficiency",
                "--disable-features=PrivacySandboxAdFledgePerformance",
                "--disable-features=PrivacySandboxAdFledgeStability",
                "--disable-features=PrivacySandboxAdFledgeReliability",
                "--disable-features=PrivacySandboxAdFledgeConfidence",
                "--disable-features=PrivacySandboxAdFledgeTrust",
                "--disable-features=PrivacySandboxAdFledgePrivacy",
                "--disable-features=PrivacySandboxAdFledgeSafety",
                "--disable-features=PrivacySandboxAdFledgeSecurity",
                "--disable-features=PrivacySandboxAdFledgeProtection",
                "--disable-features=PrivacySandboxAdFledgeEnforcement",
                "--disable-features=PrivacySandboxAdFledgeRegulation",
                "--disable-features=PrivacySandboxAdFledgeCompliance",
                "--disable-features=PrivacySandboxAdFledgeGovernance",
                "--disable-features=PrivacySandboxAdFledgeSupervision",
                "--disable-features=PrivacySandboxAdFledgeAdministration",
                "--disable-features=PrivacySandboxAdFledgeManagement",
                "--disable-features=PrivacySandboxAdFledgeConfiguration",
                "--disable-features=PrivacySandboxAdFledgePreferences",
                "--disable-features=PrivacySandboxAdFledgeSettings",
                "--disable-features=PrivacySandboxAdFledgePolicy",
                "--disable-features=PrivacySandboxAdFledgeControl",
                "--disable-features=PrivacySandboxAdFledgeAudit",
                "--disable-features=PrivacySandboxAdFledgeLogging",
                "--disable-features=PrivacySandboxAdFledgeMetrics",
                "--disable-features=PrivacySandboxAdFledgeMonitor",
                "--disable-features=PrivacySandboxAdFledgeAnalytics",
                "--disable-features=PrivacySandboxAdFledgeReport",
                "--disable-features=PrivacySandboxAdFledgeAdmin",
                "--disable-features=PrivacySandboxAdFledgeUser",
                "--disable-features=PrivacySandboxAdFledgeProfile",
                "--disable-features=PrivacySandboxAdFledgeTest",
                "--disable-features=PrivacySandboxAdFledgeDebug",
                "--disable-features=PrivacySandboxAdFledgeConsole",
                "--disable-features=PrivacySandboxAdFledgeConsent",
                "--disable-features=PrivacySandboxAdFledgeShield",
                "--disable-features=PrivacySandboxAdFledgeClient",
                "--disable-features=PrivacySandboxAdFledgeServer",
                "--disable-features=PrivacySandboxAdFledge",
                "--disable-features=PrivacySandboxAdTopics",
                "--disable-features=PrivacySandboxAdMeasurement",
                "--disable-features=PrivacySandboxAttribution",
                "--disable-features=PrivacySandboxThirdPartySets",
                "--disable-features=PrivacySandboxSameOriginTrials",
                "--disable-features=PrivacySandboxFirstPartySets",
                "--disable-features=PrivacySandboxAdsAPIs",
                "--disable-features=Fledge",
                "--disable-features=InterestFedBasedClustering",
                "--disable-features=FederatedLearningOfCohorts",
                "--disable-features=PrivacySandboxSettings",
                "--disable-features=PrivacySandboxSettings4",
                "--disable-features=WebXR",
                "--disable-features=WebUSB",
                "--disable-features=WebUIDarkMode",
                "--disable-features=TranslateUI",
                "--disable-features=TopSites",
                "--disable-features=BlinkGenPropertyTrees",
                "--disable-features=Translate",
                "--disable-features=MediaRouter",
                "--disable-features=DialMediaRouteProvider",
                "--disable-features=CalculateNativeWinOcclusion",
                "--disable-features=NetworkServiceInProcess",
                "--disable-features=NetworkService",
                "--disable-features=breakpad",
                "--disable-features=AutomationControlled",
                "--disable-features=ScriptStreaming",
                "--disable-session-crashed-bubble",
                "--disable-print-preview",
                "--disable-domain-reliability",
                "--enable-automation",
                "--ignore-certificate-errors-spki-list",
                "--ignore-certificate-errors",
                "--disable-setuid-sandbox",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-infobars",
                "--disable-features=GlobalMediaControls",
                "--disable-web-security",
                "--allow-running-insecure-content",
                "--disable-web-security",
                "--disable-speech-api",
                "--disable-permissions-api",
                "--disable-notifications",
                "--use-mock-keychain",
                "--password-store=basic",
                "--disable-ipc-flooding-protection",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--disable-prompt-on-repost",
                "--disable-popup-blocking",
                "--disable-client-side-phishing-detection",
                "--disable-hang-monitor",
                "--metrics-recording-only",
                "--disable-translate",
                "--disable-sync",
                "--disable-background-networking",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
                "--disable-component-extensions-with-background-pages",
                "--disable-features=TranslateUI",
                "--disable-extensions",
                "--disable-features=site-per-process,IsolateOrigins",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-blink-features=AutomationControlled",
            ],
        }

        # If using proxy, add proxy settings
        if use_proxy and proxy_url:
            options["args"].append(f"--proxy-server={proxy_url}")

        return options
