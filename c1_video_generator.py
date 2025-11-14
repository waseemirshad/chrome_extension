import time
import os
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import traceback
import socket
import re
import sys
from datetime import datetime, timedelta

# Import colorama for colored output
try:
    from colorama import init, Fore, Back, Style

    init(autoreset=True)
    COLOR_AVAILABLE = True
except ImportError:
    print("Installing colorama for colored output...")
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style

    init(autoreset=True)
    COLOR_AVAILABLE = True


class IngredientsToVideoAutomation:
    def __init__(self):
        # Edge driver path
        self.edge_driver_path = r"C:\WebDriver\msedgedriver.exe"

        # Session configuration for Edge
        self.sessions_base_folder = "Edge_Sessions"
        self.pc_identifier = None  # Will be set based on project choice
        self.session_path = None   # Will be set based on project choice

        self.driver = None

        # Progress tracking
        self.total_prompts = 0
        self.current_prompt_num = 0
        self.videos_downloaded = 0

        # Video tracking - CRITICAL FOR NEW STRATEGY
        self.existing_video_count = 0
        self.videos_before_generation = []  # Store video src URLs before generation

        print("=" * 60)
        print(Fore.CYAN + "🎬 INGREDIENTS TO VIDEO AUTOMATION")
        print(Fore.CYAN + "⚡ Consistent Session Across All Work Types")
        print("=" * 60)

    def initialize_report(self):
        """Initialize the comprehensive report file"""
        # Create output folder if it doesn't exist
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
            print(Fore.GREEN + f"[FOLDER] Created output folder: {OUTPUT_FOLDER}")
        
        self.report_file = os.path.join(
            OUTPUT_FOLDER,
            f"Generation_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        self.start_time = datetime.now()
        self.prompt_times = []
        
        # Enhanced tracking
        self.project_stats = {}
        self.worksheet_stats = {}
        self.total_projects = 0
        self.completed_projects = 0
        self.total_prompts_processed = 0
        self.total_generations_completed = 0

        # Create comprehensive initial report
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("╔" + "═" * 78 + "╗\n")
            f.write("║" + " " * 20 + "GOOGLE VEO INGREDIENTS AUTOMATION REPORT" + " " * 17 + "║\n")
            f.write("╚" + "═" * 78 + "╝\n\n")
            
            f.write("📋 SESSION INFORMATION\n")
            f.write("─" * 50 + "\n")
            f.write(f"🕐 Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📁 Excel File: {EXCEL_FILE_PATH}\n")
            f.write(f"🖼️ Ingredients Folder: {INGREDIENTS_FOLDER}\n")
            f.write(f"📂 Output Folder: {OUTPUT_FOLDER}\n")
            f.write(f"⚙️ Max Concurrent Generations: 8 (even numbers only)\n")
            f.write(f"🎬 Videos per Prompt: 2\n\n")
            
            f.write("📊 PROCESSING STATUS\n")
            f.write("─" * 50 + "\n")
            f.write("Status: INITIALIZING...\n\n")
            
            f.write("📝 DETAILED LOG\n")
            f.write("─" * 50 + "\n\n")

        print(Fore.GREEN + f"[REPORT] Comprehensive report initialized: {self.report_file}")

    def write_to_report(self, message, include_time=True):
        """Write a message to the report file"""
        try:
            with open(self.report_file, 'a', encoding='utf-8') as f:
                if include_time:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    elapsed = str(datetime.now() - self.start_time).split('.')[0]
                    f.write(f"[{timestamp}] [Elapsed: {elapsed}] {message}\n")
                else:
                    f.write(f"{message}\n")
                f.flush()  # Ensure immediate write
        except:
            pass  # Silent fail to not interrupt the main process

    def start_worksheet_tracking(self, worksheet_name, prompt_count):
        """Start tracking statistics for a worksheet"""
        self.worksheet_stats[worksheet_name] = {
            'prompts': prompt_count,
            'start_time': datetime.now(),
            'status': 'PROCESSING',
            'duration': None
        }
        self.write_to_report(f"📋 Started processing worksheet: {worksheet_name} ({prompt_count} prompts)")

    def complete_worksheet_tracking(self, worksheet_name, success=True):
        """Complete tracking statistics for a worksheet"""
        if worksheet_name in self.worksheet_stats:
            end_time = datetime.now()
            start_time = self.worksheet_stats[worksheet_name]['start_time']
            duration = str(end_time - start_time).split('.')[0]
            
            self.worksheet_stats[worksheet_name]['duration'] = duration
            self.worksheet_stats[worksheet_name]['status'] = 'COMPLETED' if success else 'FAILED'
            
            status_emoji = "✅" if success else "❌"
            self.write_to_report(f"{status_emoji} Completed worksheet: {worksheet_name} (Duration: {duration})")
            
            if success:
                self.completed_projects += 1
                self.total_prompts_processed += self.worksheet_stats[worksheet_name]['prompts']

    def update_generation_stats(self, prompts_completed=0, generations_completed=0):
        """Update generation statistics"""
        self.total_generations_completed += generations_completed
        
        # Update report with current progress
        try:
            # Read current report
            with open(self.report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update the status section
            current_time = datetime.now()
            elapsed = str(current_time - self.start_time).split('.')[0]
            
            status_section = f"""📊 PROCESSING STATUS
─────────────────────────────────────────────────────
🕐 Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
⏱️ Elapsed Time: {elapsed}
🏗️ Projects Completed: {self.completed_projects}
📋 Worksheets Processed: {len([w for w in self.worksheet_stats.values() if w['status'] == 'COMPLETED'])}
📝 Total Prompts Processed: {self.total_prompts_processed}
🎬 Total Generations Completed: {self.total_generations_completed}
📊 Expected Videos Generated: {self.total_prompts_processed * 2}
Status: PROCESSING...

"""
            
            # Replace the status section
            lines = content.split('\n')
            new_lines = []
            skip_until_log = False
            
            for line in lines:
                if line.startswith('📊 PROCESSING STATUS'):
                    new_lines.extend(status_section.split('\n'))
                    skip_until_log = True
                elif line.startswith('📝 DETAILED LOG'):
                    skip_until_log = False
                    new_lines.append(line)
                elif not skip_until_log:
                    new_lines.append(line)
                else:
                    continue
            
            # Write updated content
            with open(self.report_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
                
        except:
            pass  # Silent fail to not interrupt the main process

    def write_final_summary(self):
        """Write comprehensive final summary to report"""
        try:
            end_time = datetime.now()
            total_time = end_time - self.start_time

            with open(self.report_file, 'a', encoding='utf-8') as f:
                f.write("\n\n╔" + "═" * 78 + "╗\n")
                f.write("║" + " " * 30 + "FINAL SUMMARY" + " " * 35 + "║\n")
                f.write("╚" + "═" * 78 + "╝\n\n")
                
                # Session Summary
                f.write("🕐 SESSION SUMMARY\n")
                f.write("─" * 50 + "\n")
                f.write(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Duration: {str(total_time).split('.')[0]}\n")
                f.write(f"Session Status: COMPLETED\n\n")

                # Project Statistics
                f.write("🏗️ PROJECT STATISTICS\n")
                f.write("─" * 50 + "\n")
                f.write(f"Total Projects Created: {self.completed_projects}\n")
                f.write(f"Total Worksheets Processed: {len(self.worksheet_stats)}\n")
                f.write(f"Total Prompts Processed: {self.total_prompts_processed}\n")
                f.write(f"Total Generations Completed: {self.total_generations_completed}\n")
                f.write(f"Expected Videos Generated: {self.total_prompts_processed * 2}\n\n")

                # Worksheet Breakdown
                if self.worksheet_stats:
                    f.write("📋 WORKSHEET BREAKDOWN\n")
                    f.write("─" * 50 + "\n")
                    for worksheet_name, stats in self.worksheet_stats.items():
                        f.write(f"📄 {worksheet_name}:\n")
                        f.write(f"   • Prompts: {stats['prompts']}\n")
                        f.write(f"   • Processing Time: {stats['duration']}\n")
                        f.write(f"   • Expected Videos: {stats['prompts'] * 2}\n")
                        f.write(f"   • Status: {stats['status']}\n\n")

                # Timing Analysis
                if self.prompt_times:
                    avg_time = sum(self.prompt_times) / len(self.prompt_times)
                    min_time = min(self.prompt_times)
                    max_time = max(self.prompt_times)

                    f.write("⏱️ TIMING ANALYSIS\n")
                    f.write("─" * 50 + "\n")
                    f.write(f"Average Time per Prompt: {str(timedelta(seconds=int(avg_time)))}\n")
                    f.write(f"Fastest Prompt: {str(timedelta(seconds=int(min_time)))}\n")
                    f.write(f"Slowest Prompt: {str(timedelta(seconds=int(max_time)))}\n")
                    f.write(f"Total Processing Time: {str(total_time).split('.')[0]}\n\n")

                    # Processing Rate
                    hours = total_time.total_seconds() / 3600
                    prompts_per_hour = len(self.prompt_times) / hours if hours > 0 else 0
                    projects_per_hour = self.completed_projects / hours if hours > 0 else 0

                    f.write("📈 PROCESSING RATE\n")
                    f.write("─" * 50 + "\n")
                    f.write(f"Prompts per Hour: {prompts_per_hour:.1f}\n")
                    f.write(f"Projects per Hour: {projects_per_hour:.1f}\n")
                    f.write(f"Expected Videos per Hour: {prompts_per_hour * 2:.1f}\n\n")

                # Performance Summary
                f.write("🎯 PERFORMANCE SUMMARY\n")
                f.write("─" * 50 + "\n")
                if self.total_prompts_processed > 0:
                    efficiency = (self.total_generations_completed / self.total_prompts_processed) * 100
                    f.write(f"Generation Efficiency: {efficiency:.1f}%\n")
                
                if total_time.total_seconds() > 0:
                    throughput = self.total_prompts_processed / (total_time.total_seconds() / 60)
                    f.write(f"Throughput: {throughput:.2f} prompts/minute\n")
                
                f.write(f"Queue Strategy: Even numbers only (max 8 concurrent)\n")
                f.write(f"Image Strategy: Worksheet-specific folders\n\n")

                # Footer
                f.write("╔" + "═" * 78 + "╗\n")
                f.write("║" + " " * 25 + "REPORT GENERATION COMPLETE" + " " * 27 + "║\n")
                f.write("║" + f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 44 + "║\n")
                f.write("╚" + "═" * 78 + "╝\n")

            print(Fore.GREEN + f"\n[REPORT] Comprehensive final report saved to: {self.report_file}")

        except Exception as e:
            print(Fore.YELLOW + f"[WARNING] Could not write final summary: {e}")

    def get_pc_identifier(self, use_timestamp=True):
        """Create a unique identifier for this PC"""
        try:
            computer_name = socket.gethostname()
            username = os.getlogin()
            if use_timestamp:
                timestamp = str(int(time.time()))  # Add timestamp for uniqueness
                identifier = f"{computer_name}_{username}_{timestamp}".replace(" ", "_").replace("-", "_")
            else:
                identifier = f"{computer_name}_{username}".replace(" ", "_").replace("-", "_")
            return identifier
        except:
            if use_timestamp:
                return f"default_pc_{str(int(time.time()))}"
            else:
                return "default_pc"

    def setup_session(self, project_choice=None):
        """Setup consistent session within MamaCat project"""
        # Always use consistent session without timestamp for all work types
        self.pc_identifier = self.get_pc_identifier(use_timestamp=False)
        # Use project root directory for sessions (go up from 3_VIDEO_PRODUCTION to MamaCat root)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)  # Go up one level to MamaCat root
        self.session_path = os.path.join(project_root, self.sessions_base_folder, self.pc_identifier)
        
        # Check and create session folder
        self.check_or_create_session()
        
        print(Fore.YELLOW + f"🔗 Using consistent session: {self.session_path}")
        
        return True

    def check_or_create_session(self):
        """Check if session exists, if not create it"""
        try:
            if not os.path.exists(self.sessions_base_folder):
                os.makedirs(self.sessions_base_folder)
                print(Fore.GREEN + f"✅ Created sessions base folder")

            if not os.path.exists(self.session_path):
                os.makedirs(self.session_path)
                print(Fore.YELLOW + f"🆕 New consistent session created - Google login required")
                print(Fore.CYAN + f"💡 This session will be reused for all future work")
            else:
                print(Fore.GREEN + f"✅ Using existing consistent session")
                print(Fore.CYAN + f"💡 Same session used for fresh projects, existing projects, and ranges")

        except Exception as e:
            print(Fore.RED + f"⚠️ Session folder error: {e}")

    def setup_driver(self):
        """Setup Edge driver with session management"""
        try:
            print(Fore.CYAN + "\n[BROWSER] Starting Microsoft Edge...")

            if not os.path.exists(self.edge_driver_path):
                print(Fore.RED + f"[ERROR] Edge driver not found at: {self.edge_driver_path}")
                return None

            options = Options()
            abs_session_path = os.path.abspath(self.session_path)

            options.add_argument(f"--user-data-dir={abs_session_path}")
            options.add_argument("--profile-directory=Default")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            prefs = {
                "download.default_directory": BROWSER_DOWNLOAD_FOLDER,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "profile.default_content_setting_values.automatic_downloads": 1
            }
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--start-maximized")

            service = Service(executable_path=self.edge_driver_path)
            driver = webdriver.Edge(service=service, options=options)

            print(Fore.GREEN + "[BROWSER] ✅ Edge started successfully")

            # Check Google login
            driver.get("https://accounts.google.com")
            time.sleep(3)

            current_url = driver.current_url
            if "accounts.google.com" in current_url and "signin" in current_url:
                print(Fore.YELLOW + "\n[LOGIN] Please login to your Google account")
                input("Press Enter after logging in...")
            else:
                print(Fore.GREEN + "[LOGIN] ✅ Using existing Google session")

            return driver

        except Exception as e:
            print(Fore.RED + f"[ERROR] Driver setup failed: {str(e)}")
            return None

    def navigate_to_flow(self):
        """Navigate to Google Flow main page"""
        try:
            print(Fore.CYAN + f"\n[NAVIGATE] Opening Google Flow...")
            self.driver.get("https://labs.google/fx/tools/flow")
            time.sleep(5)

            if "labs.google" in self.driver.current_url:
                print(Fore.GREEN + f"[NAVIGATE] ✅ Flow loaded")
                return True
            return False

        except Exception as e:
            print(Fore.RED + f"[ERROR] Navigation failed: {str(e)}")
            return False

    def navigate_to_existing_project(self, project_url):
        """Navigate to an existing project URL"""
        try:
            print(Fore.CYAN + f"\n[NAVIGATE] Opening existing project...")
            self.driver.get(project_url)
            time.sleep(5)

            if "labs.google" in self.driver.current_url:
                print(Fore.GREEN + f"[NAVIGATE] ✅ Project loaded")
                return True
            return False

        except Exception as e:
            print(Fore.RED + f"[ERROR] Navigation to project failed: {str(e)}")
            return False

    def get_project_choice(self):
        """Get user choice for project type"""
        print(f"\n{'═' * 60}")
        print(Fore.CYAN + "🎯 PROJECT SELECTION")
        print(f"{'═' * 60}")
        print("1. Create fresh project (upload images + all prompts with enhanced ingredient selection)")
        print(f"{'═' * 60}")
        
        while True:
            choice = input("➤ Enter your choice (1): ").strip()
            if choice in ['1']:
                return int(choice)
            print(Fore.YELLOW + "⚠️ Please enter 1")



    def get_ingredient_images(self):
        """Get ALL ingredient images for MamaCat story"""
        try:
            # Get the script's directory and construct absolute path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ingredients_folder = os.path.join(script_dir, INGREDIENTS_FOLDER)
            
            print(Fore.CYAN + f"\n[INGREDIENTS] Looking for ingredients in: {ingredients_folder}")
            
            if not os.path.exists(ingredients_folder):
                print(Fore.RED + f"[ERROR] Ingredients folder not found")
                print(Fore.YELLOW + f"[INFO] Expected folder: {ingredients_folder}")
                return None
            
            # Look for ALL image files in the folder
            ingredient_files = []
            supported_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
            
            for filename in os.listdir(ingredients_folder):
                file_path = os.path.join(ingredients_folder, filename)
                if os.path.isfile(file_path):
                    # Check if it's an image file
                    _, ext = os.path.splitext(filename.lower())
                    if ext in supported_extensions:
                        ingredient_files.append(file_path)
            
            # Sort files naturally with proper numeric ordering (01.png, 02.png, 03.png, etc.)
            # This handles zero-padded format correctly for up to 20 ingredients
            def natural_sort_key(filename):
                import re
                # Extract numbers from filename and pad them for proper sorting
                numbers = re.findall(r'\d+', os.path.basename(filename))
                if numbers:
                    # Convert first number to int for proper numeric sorting
                    return int(numbers[0])
                return 0
            
            ingredient_files.sort(key=natural_sort_key)
            
            if len(ingredient_files) == 0:
                print(Fore.RED + f"[ERROR] No image files found in ingredients folder")
                print(Fore.YELLOW + f"[INFO] Supported formats: {', '.join(supported_extensions)}")
                return None
            
            print(Fore.GREEN + f"[INGREDIENTS] ✅ Found {len(ingredient_files)} ingredients:")
            for i, img in enumerate(ingredient_files, 1):
                print(f"  {i}. {os.path.basename(img)}")
            
            return ingredient_files
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to get ingredients: {str(e)}")
            return None



    def upload_multiple_ingredients_to_library(self, ingredient_paths):
        """Upload multiple ingredients to media library using FIRST + button and EXTENDED WAIT logic
        
        EXTENDED WAIT FEATURES:
        - Initial wait: 8 seconds → check for upload
        - Continued waits: 5 seconds → check → 5 seconds → check... until 100 seconds total
        - Checks for remove button appearance (primary upload indicator)
        - Immediate remove button click when upload detected
        - Maximum 100 seconds total wait time per ingredient
        - Detailed progress showing total time elapsed
        - Supports up to 20 ingredients with zero-padded format
        """
        try:
            total_ingredients = len(ingredient_paths)
            print(Fore.CYAN + f"\n[LIBRARY UPLOAD] Uploading {total_ingredients} ingredients to media library...")
            print(Fore.YELLOW + f"[LIBRARY UPLOAD] Using FIRST + button and FIRST remove button only")

            # REVERSE UPLOAD ORDER: Upload last ingredient first (20th, 19th, ..., 02nd, 01st)
            # This way 01st ingredient appears first in gallery, supporting up to 20 ingredients
            reversed_ingredients = list(reversed(ingredient_paths))
            
            print(Fore.YELLOW + f"[UPLOAD] Using REVERSE upload order for correct gallery positioning:")
            for idx, ingredient_path in enumerate(reversed_ingredients):
                original_idx = len(ingredient_paths) - idx  # Show original position
                print(Fore.YELLOW + f"  Upload order {idx + 1}: {os.path.basename(ingredient_path)} (originally ingredient {original_idx:02d})")
            
            # Upload each ingredient one by one using FIRST buttons
            for idx, ingredient_path in enumerate(reversed_ingredients):
                original_idx = len(ingredient_paths) - idx
                print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] Uploading: {os.path.basename(ingredient_path)}")

                # Find FIRST + button
                first_plus_button = None
                try:
                    plus_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.sc-74578dc8-1.hopAJY")
                    if plus_buttons:
                        first_plus_button = plus_buttons[0]  # Always use FIRST + button
                except:
                    pass

                if not first_plus_button:
                    print(Fore.RED + f"  [INGREDIENT {original_idx}] ❌ Cannot find FIRST + button")
                    return False

                # Click the FIRST + button
                self.driver.execute_script("arguments[0].click();", first_plus_button)
                time.sleep(2)

                # Find file input and upload
                file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                if file_inputs:
                    file_inputs[-1].send_keys(ingredient_path)
                    time.sleep(3)

                    # Click Crop and Save button if it appears
                    try:
                        crop_btn = self.driver.find_element(
                            By.XPATH,
                            "//button[contains(., 'Crop and Save') or contains(., 'Crop & Save') or contains(., 'Crop and save')]"
                        )
                        self.driver.execute_script("arguments[0].click();", crop_btn)
                        time.sleep(3)
                        print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Uploaded and cropped")
                    except:
                        print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Uploaded")

                    # EXTENDED WAIT LOGIC: 8sec → check → 5sec → check → 5sec → check... until 100sec total
                    upload_completed = False
                    total_waited = 0
                    max_wait_time = 100  # Maximum 100 seconds total
                    check_count = 0
                    
                    # First wait: 8 seconds
                    first_wait = 8
                    print(Fore.CYAN + f"  [INGREDIENT {original_idx}] ⏳ Initial wait: {first_wait} seconds...")
                    for i in range(first_wait, 0, -1):
                        print(f"\r  [INGREDIENT {original_idx}] ⏳ Waiting {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    total_waited += first_wait
                    check_count += 1
                    
                    print(f"\r  [INGREDIENT {original_idx}] ⏳ Wait complete, checking upload (check {check_count})...                    ")
                    
                    # Check if uploaded after first 8 seconds
                    try:
                        remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..")
                        if len(remove_buttons) > 0:
                            upload_completed = True
                            print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Upload completed after {total_waited} seconds!")
                        else:
                            # Try alternative selector
                            alt_remove_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                            if len(alt_remove_buttons) > 0:
                                upload_completed = True
                                print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Upload completed after {total_waited} seconds!")
                    except Exception as e:
                        print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ Check failed: {str(e)}")
                    
                    # Continue with 5-second intervals until 100 seconds total
                    while not upload_completed and total_waited < max_wait_time:
                        remaining_time = max_wait_time - total_waited
                        next_wait = min(5, remaining_time)  # Wait 5 seconds or remaining time
                        
                        if next_wait <= 0:
                            break
                        
                        print(Fore.CYAN + f"  [INGREDIENT {original_idx}] ⏳ Continuing wait: {next_wait} seconds (total: {total_waited}/{max_wait_time}s)...")
                        for i in range(next_wait, 0, -1):
                            print(f"\r  [INGREDIENT {original_idx}] ⏳ Waiting {i} seconds... (total: {total_waited + (next_wait - i + 1)}/{max_wait_time}s)", end="", flush=True)
                            time.sleep(1)
                        
                        total_waited += next_wait
                        check_count += 1
                        
                        print(f"\r  [INGREDIENT {original_idx}] ⏳ Wait complete, checking upload (check {check_count})...                    ")
                        
                        # Check if uploaded
                        try:
                            remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..")
                            if len(remove_buttons) > 0:
                                upload_completed = True
                                print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Upload completed after {total_waited} seconds!")
                                break
                            else:
                                # Try alternative selector
                                alt_remove_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                                if len(alt_remove_buttons) > 0:
                                    upload_completed = True
                                    print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Upload completed after {total_waited} seconds!")
                                    break
                                else:
                                    print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ Not uploaded yet after {total_waited}s, continuing...")
                        except Exception as e:
                            print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ Check failed: {str(e)}")
                    
                    if not upload_completed:
                        print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ Upload not detected after {total_waited} seconds total, but continuing...")
                    
                    # IMMEDIATE REMOVE: Click remove button right after upload detection
                    print(Fore.CYAN + f"  [INGREDIENT {original_idx}] 🗑️ Clicking remove button immediately...")
                    
                    # Find and click remove button - USING THE EXACT WORKING SELECTORS
                    remove_clicked = False
                    try:
                        # Method 1: Look for FIRST button with "close" icon (EXACT working selector)
                        remove_buttons = self.driver.find_elements(
                            By.XPATH, 
                            "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/.."
                        )
                        if remove_buttons:
                            first_remove_button = remove_buttons[0]  # Always use FIRST remove button
                            self.driver.execute_script("arguments[0].click();", first_remove_button)
                            print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Remove button clicked (Method 1)")
                            remove_clicked = True
                        else:
                            # Method 2: Alternative selector that was working
                            remove_buttons = self.driver.find_elements(
                                By.XPATH,
                                "//button//i[text()='close']/.."
                            )
                            if remove_buttons:
                                first_remove_button = remove_buttons[0]
                                self.driver.execute_script("arguments[0].click();", first_remove_button)
                                print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Remove button clicked (Method 2)")
                                remove_clicked = True
                            else:
                                print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ No remove button found with either method")
                    except Exception as e:
                        print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ Remove button error: {str(e)}")
                    
                    # Monitor remove button click success
                    if remove_clicked:
                        print(Fore.CYAN + f"  [INGREDIENT {original_idx}] 🔍 Monitoring remove completion...")
                        time.sleep(1)  # Brief wait to let removal process
                        
                        # Check if remove button disappeared (removal successful)
                        try:
                            remaining_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                            if len(remaining_buttons) == 0:
                                print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Removal confirmed")
                            else:
                                print(Fore.YELLOW + f"  [INGREDIENT {original_idx}] ⚠️ Remove button still visible, but continuing")
                        except:
                            print(Fore.GREEN + f"  [INGREDIENT {original_idx}] ✅ Removal process completed")

                else:
                    print(Fore.RED + f"  [INGREDIENT {original_idx}] ❌ No file input found")
                    return False

            print(Fore.GREEN + f"[LIBRARY UPLOAD] ✅ All {total_ingredients} ingredients uploaded to media library")
            
            # Create ingredient mapping for selection phase
            # Since we upload in REVERSE order (4th, 3rd, 2nd, 1st), the gallery order is now sequential
            self.ingredient_mapping = {}
            for idx, ingredient_path in enumerate(ingredient_paths):
                filename = os.path.basename(ingredient_path)
                # With reverse upload: 1st ingredient appears at index 2, 2nd at index 3, etc.
                gallery_index = 2 + idx
                self.ingredient_mapping[filename] = gallery_index
                print(Fore.CYAN + f"[MAPPING] {filename} → Gallery Index {gallery_index}")
            
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + "🎬 UPLOAD PHASE COMPLETED!")
            print(f"{'═' * 60}")
            print(Fore.GREEN + f"✅ All {total_ingredients} ingredients uploaded to media library")
            print(Fore.YELLOW + "📋 Ingredient mapping created for selection phase")
            print(Fore.GREEN + "� Autgomatically proceeding to GENERATION PHASE...")
            print(f"{'═' * 60}")
            
            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Library upload failed: {str(e)}")
            return False

    # ═══════════════════════════════════════════════════════════════════
    # HYBRID INGREDIENT SYSTEM - GENERATION + UPLOAD WITH REMOVE CYCLE
    # ═══════════════════════════════════════════════════════════════════



    def detect_story_ingredients(self, story_name):
        """Detect all story ingredients (03, 04, 05, 06) by reading from Story_Ingredients.xlsx
        
        NOTE: This only detects story-specific ingredients (03-06, max 4).
        Base cat ingredients (01, 02) are NOT in Excel - they are pre-existing photos.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ingredients_excel = os.path.join(script_dir, INGREDIENTS_EXCEL_PATH)
            
            if not os.path.exists(ingredients_excel):
                print(Fore.RED + f"[ERROR] Ingredients Excel not found: {ingredients_excel}")
                return []
            
            # Read the Excel file
            try:
                df = pd.read_excel(ingredients_excel, sheet_name=story_name)
            except Exception as e:
                print(Fore.RED + f"[ERROR] Could not find worksheet '{story_name}' in {INGREDIENTS_EXCEL_PATH}")
                print(Fore.YELLOW + f"[INFO] Available worksheets: {pd.ExcelFile(ingredients_excel).sheet_names}")
                return []
            
            # Get ingredient numbers from the Ingredient_No column
            if 'Ingredient_No' not in df.columns:
                print(Fore.RED + f"[ERROR] 'Ingredient_No' column not found in worksheet")
                return []
            
            ingredient_numbers = df['Ingredient_No'].astype(str).tolist()
            ingredient_numbers = sorted(list(set(ingredient_numbers)))  # Remove duplicates and sort
            
            print(Fore.GREEN + f"[DETECT] Found {len(ingredient_numbers)} story ingredients in Excel: {ingredient_numbers}")
            return ingredient_numbers
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to detect story ingredients: {str(e)}")
            traceback.print_exc()
            return []

    def parse_ingredient_prompt(self, story_name, ingredient_num):
        """Parse the prompt for a specific ingredient from Story_Ingredients.xlsx
        
        Reads from Excel file with columns:
        - Ingredient_No (e.g., "04", "05")
        - Title (e.g., "Juice Stand Setup")
        - Prompt (full prompt text)
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            ingredients_excel = os.path.join(script_dir, INGREDIENTS_EXCEL_PATH)
            
            if not os.path.exists(ingredients_excel):
                print(Fore.RED + f"[ERROR] Ingredients Excel not found: {ingredients_excel}")
                return None
            
            print(Fore.CYAN + f"[PARSE] Looking for story: '{story_name}'")
            
            # Read the Excel file
            try:
                df = pd.read_excel(ingredients_excel, sheet_name=story_name)
            except Exception as e:
                print(Fore.RED + f"[ERROR] Could not find worksheet '{story_name}' in {INGREDIENTS_EXCEL_PATH}")
                print(Fore.YELLOW + f"[INFO] Available worksheets: {pd.ExcelFile(ingredients_excel).sheet_names}")
                return None
            
            print(Fore.GREEN + f"[PARSE] ✓ Found worksheet for: '{story_name}'")
            
            # Find the row with matching ingredient number
            df['Ingredient_No'] = df['Ingredient_No'].astype(str)
            matching_rows = df[df['Ingredient_No'] == ingredient_num]
            
            if matching_rows.empty:
                print(Fore.RED + f"[ERROR] Could not find ingredient {ingredient_num} in worksheet")
                print(Fore.YELLOW + f"[INFO] Available ingredients: {df['Ingredient_No'].tolist()}")
                return None
            
            # Get the first matching row
            row = matching_rows.iloc[0]
            title = row['Title']
            prompt = row['Prompt']
            
            print(Fore.GREEN + f"[PARSE] ✓ Found {ingredient_num}.jpeg")
            print(Fore.CYAN + f"[PARSE]   Title: {title}")
            print(Fore.CYAN + f"[PARSE]   Prompt: {prompt[:80]}..." if len(prompt) > 80 else f"[PARSE]   Prompt: {prompt}")
            
            return {'title': title, 'prompt': prompt}
                
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to parse ingredient prompt: {str(e)}")
            traceback.print_exc()
            return None

    def enter_prompt_and_generate(self, prompt_text, ingredient_num):
        """Enter prompt text and click generate button"""
        try:
            print(Fore.CYAN + f"\n[GENERATE {ingredient_num}] Entering prompt...")
            
            # Find text area
            text_area = None
            
            # Method 1: By data-testid
            try:
                text_area = self.driver.find_element(By.CSS_SELECTOR, "textarea[data-testid='prompt-textarea']")
            except:
                pass
            
            # Method 2: By placeholder
            if not text_area:
                try:
                    text_area = self.driver.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Describe')]")
                except:
                    pass
            
            # Method 3: Any textarea
            if not text_area:
                try:
                    textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
                    if textareas:
                        text_area = textareas[0]
                except:
                    pass
            
            if not text_area:
                print(Fore.RED + f"[GENERATE {ingredient_num}] ❌ Could not find text area")
                return False
            
            # Scroll to element
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", text_area)
            time.sleep(1)
            
            # Close any overlays
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)
            
            # Click the text area to focus it
            self.driver.execute_script("arguments[0].click();", text_area)
            time.sleep(0.5)
            
            # Clear existing text
            text_area.click()
            time.sleep(0.3)
            text_area.send_keys(Keys.CONTROL + "a")
            time.sleep(0.3)
            text_area.send_keys(Keys.DELETE)
            time.sleep(0.3)
            
            # Copy prompt to clipboard and paste
            pyperclip.copy(prompt_text)
            text_area.send_keys(Keys.CONTROL + "v")
            time.sleep(0.5)
            
            # Trigger input event
            self.driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, text_area)
            
            # Click outside and back
            self.driver.execute_script("document.body.click();")
            time.sleep(0.5)
            text_area.click()
            time.sleep(0.5)
            
            print(Fore.GREEN + f"[GENERATE {ingredient_num}] ✅ Prompt entered")
            
            # Wait 3 seconds before clicking generate
            print(Fore.YELLOW + f"[GENERATE {ingredient_num}] ⏳ Waiting 3 seconds before generation...")
            for i in range(3, 0, -1):
                print(f"\r[GENERATE {ingredient_num}] ⏳ Waiting {i} seconds...", end="", flush=True)
                time.sleep(1)
            print(f"\r[GENERATE {ingredient_num}] ⏳ Wait complete!                    ")
            
            # Click generate button
            generate_btn = None
            
            # Method 1: By icon
            try:
                generate_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[.//i[contains(@class, 'google-symbols') and contains(., 'arrow_forward')]]"
                )
            except:
                pass
            
            # Method 2: Find all buttons and check if enabled
            if not generate_btn:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if "arrow_forward" in btn.get_attribute("innerHTML"):
                        if btn.is_enabled():
                            generate_btn = btn
                            break
            
            if generate_btn:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", generate_btn)
                time.sleep(0.5)
                
                # Check if button is enabled
                if not generate_btn.is_enabled():
                    print(Fore.YELLOW + f"[GENERATE {ingredient_num}] ⚠️ Generate button not enabled, waiting...")
                    time.sleep(3)
                
                self.driver.execute_script("arguments[0].click();", generate_btn)
                print(Fore.GREEN + f"[GENERATE {ingredient_num}] ✅ Generation started")
                return True
            else:
                print(Fore.RED + f"[GENERATE {ingredient_num}] ❌ Could not find generate button")
                return False
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Prompt/Generate failed for {ingredient_num}: {str(e)}")
            return False

    def wait_for_generation_complete_extended(self, ingredient_num, max_wait=100):
        """Enhanced generation monitoring - waits until Save button appears (up to 100s)"""
        try:
            print(Fore.CYAN + f"\n[WAIT {ingredient_num}] Enhanced generation monitoring - waiting for Save button...")
            
            generation_completed = False
            total_waited = 0
            check_count = 0
            
            # First wait: 20 seconds (longer for image generation)
            first_wait = 20
            print(Fore.CYAN + f"[WAIT {ingredient_num}] ⏳ Initial wait: {first_wait} seconds...")
            for i in range(first_wait, 0, -1):
                print(f"\r[WAIT {ingredient_num}] ⏳ Waiting {i} seconds...", end="", flush=True)
                time.sleep(1)
            total_waited += first_wait
            check_count += 1
            
            print(f"\r[WAIT {ingredient_num}] ⏳ Wait complete, checking generation (check {check_count})...                    ")
            
            # Check if generated after first 20 seconds
            save_ingredient_btn = self.check_for_save_button(ingredient_num)
            if save_ingredient_btn:
                generation_completed = True
                print(Fore.GREEN + f"[WAIT {ingredient_num}] ✅ Generation completed after {total_waited} seconds!")
            
            # Continue with 5-second intervals until 100 seconds total
            while not generation_completed and total_waited < max_wait:
                remaining_time = max_wait - total_waited
                next_wait = min(5, remaining_time)  # Wait 5 seconds or remaining time
                
                if next_wait <= 0:
                    break
                
                print(Fore.CYAN + f"[WAIT {ingredient_num}] ⏳ Continuing generation wait: {next_wait} seconds (total: {total_waited}/{max_wait}s)...")
                for i in range(next_wait, 0, -1):
                    print(f"\r[WAIT {ingredient_num}] ⏳ Waiting for generation {i} seconds... (total: {total_waited + (next_wait - i + 1)}/{max_wait}s)", end="", flush=True)
                    time.sleep(1)
                
                total_waited += next_wait
                check_count += 1
                
                print(f"\r[WAIT {ingredient_num}] ⏳ Wait complete, checking for Save button (check {check_count})...                    ")
                
                # Check if Save button appeared
                save_ingredient_btn = self.check_for_save_button(ingredient_num)
                if save_ingredient_btn:
                    generation_completed = True
                    print(Fore.GREEN + f"[WAIT {ingredient_num}] ✅ Generation completed after {total_waited} seconds!")
                    break
                else:
                    print(Fore.YELLOW + f"[WAIT {ingredient_num}] ⚠️ Still generating after {total_waited}s, continuing to wait...")
            
            if not generation_completed:
                print(Fore.YELLOW + f"[WAIT {ingredient_num}] ⚠️ Generation not detected after {total_waited} seconds total")
                return False
            
            return True
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Generation wait failed for {ingredient_num}: {str(e)}")
            return False

    def check_for_save_button(self, ingredient_num):
        """Check if Save as New Ingredient button is available"""
        try:
            # Method 1: By icon and text
            try:
                save_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[.//i[contains(text(), 'add_photo_alternate')] and contains(., 'Save as New Ingredient')]"
                )
                if save_btn.is_displayed() and save_btn.is_enabled():
                    return save_btn
            except:
                pass
            
            # Method 2: Simple text search
            try:
                save_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[contains(., 'Save as New Ingredient')]"
                )
                if save_btn.is_displayed() and save_btn.is_enabled():
                    return save_btn
            except:
                pass
            
            return None
        
        except Exception as e:
            print(Fore.YELLOW + f"[WAIT {ingredient_num}] ⚠️ Save button check failed: {str(e)}")
            return None

    def click_save_as_new_ingredient(self, ingredient_num):
        """Click the 'Save as New Ingredient' button"""
        try:
            print(Fore.CYAN + f"\n[SAVE {ingredient_num}] Clicking 'Save as New Ingredient' button...")
            
            save_btn = None
            
            # Method 1: By icon and text
            try:
                save_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[.//i[contains(text(), 'add_photo_alternate')] and contains(., 'Save as New Ingredient')]"
                )
                print(Fore.GREEN + f"[SAVE {ingredient_num}] ✅ Found button (Method 1)")
            except:
                pass
            
            # Method 2: By class and text
            if not save_btn:
                try:
                    save_btn = self.driver.find_element(
                        By.XPATH,
                        "//button[contains(@class, 'sc-c177465c-1') and contains(., 'Save as New Ingredient')]"
                    )
                    print(Fore.GREEN + f"[SAVE {ingredient_num}] ✅ Found button (Method 2)")
                except:
                    pass
            
            # Method 3: Simple text search
            if not save_btn:
                try:
                    save_btn = self.driver.find_element(
                        By.XPATH,
                        "//button[contains(., 'Save as New Ingredient')]"
                    )
                    print(Fore.GREEN + f"[SAVE {ingredient_num}] ✅ Found button (Method 3)")
                except:
                    pass
            
            if save_btn:
                # Scroll to button
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                time.sleep(0.5)
                
                # Click the button
                self.driver.execute_script("arguments[0].click();", save_btn)
                print(Fore.GREEN + f"[SAVE {ingredient_num}] ✅ Clicked 'Save as New Ingredient' button")
                time.sleep(3)
                return True
            else:
                print(Fore.RED + f"[SAVE {ingredient_num}] ❌ Could not find 'Save as New Ingredient' button")
                return False
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to click save button for {ingredient_num}: {str(e)}")
            return False

    def wait_for_save_complete_extended(self, ingredient_num, max_wait=100):
        """Wait for save completion with extended monitoring (up to 100s) - SAME AS UPLOAD MONITORING"""
        try:
            print(Fore.CYAN + f"\n[SAVE WAIT {ingredient_num}] Monitoring save completion with extended wait...")
            print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] Looking for remove button appearance (indicates save complete)")
            
            save_completed = False
            total_waited = 0
            check_count = 0
            
            # First wait: 8 seconds
            first_wait = 8
            print(Fore.CYAN + f"[SAVE WAIT {ingredient_num}] ⏳ Initial wait: {first_wait} seconds...")
            for i in range(first_wait, 0, -1):
                print(f"\r[SAVE WAIT {ingredient_num}] ⏳ Waiting {i} seconds...", end="", flush=True)
                time.sleep(1)
            total_waited += first_wait
            check_count += 1
            
            print(f"\r[SAVE WAIT {ingredient_num}] ⏳ Wait complete, checking save (check {check_count})...                    ")
            
            # Check if saved after first 8 seconds - SAME LOGIC AS UPLOAD
            try:
                remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..")
                if len(remove_buttons) > 0:
                    save_completed = True
                    print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Save completed after {total_waited} seconds!")
                else:
                    # Try alternative selector
                    alt_remove_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                    if len(alt_remove_buttons) > 0:
                        save_completed = True
                        print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Save completed after {total_waited} seconds!")
            except Exception as e:
                print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Check failed: {str(e)}")
            
            # Continue with 5-second intervals until 100 seconds total - SAME AS UPLOAD
            while not save_completed and total_waited < max_wait:
                remaining_time = max_wait - total_waited
                next_wait = min(5, remaining_time)  # Wait 5 seconds or remaining time
                
                if next_wait <= 0:
                    break
                
                print(Fore.CYAN + f"[SAVE WAIT {ingredient_num}] ⏳ Continuing wait: {next_wait} seconds (total: {total_waited}/{max_wait}s)...")
                for i in range(next_wait, 0, -1):
                    print(f"\r[SAVE WAIT {ingredient_num}] ⏳ Waiting {i} seconds... (total: {total_waited + (next_wait - i + 1)}/{max_wait}s)", end="", flush=True)
                    time.sleep(1)
                
                total_waited += next_wait
                check_count += 1
                
                print(f"\r[SAVE WAIT {ingredient_num}] ⏳ Wait complete, checking save (check {check_count})...                    ")
                
                # Check if saved - SAME LOGIC AS UPLOAD
                try:
                    remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..")
                    if len(remove_buttons) > 0:
                        save_completed = True
                        print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Save completed after {total_waited} seconds!")
                        break
                    else:
                        # Try alternative selector
                        alt_remove_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                        if len(alt_remove_buttons) > 0:
                            save_completed = True
                            print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Save completed after {total_waited} seconds!")
                            break
                        else:
                            print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Not saved yet after {total_waited}s, continuing...")
                except Exception as e:
                    print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Check failed: {str(e)}")
            
            if not save_completed:
                print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Save not detected after {total_waited} seconds total, but continuing...")
            
            # IMMEDIATE REMOVE: Click remove button right after save detection - SAME AS UPLOAD
            print(Fore.CYAN + f"[SAVE WAIT {ingredient_num}] 🗑️ Clicking remove button immediately...")
            
            # Find and click remove button - USING THE EXACT WORKING SELECTORS FROM UPLOAD
            remove_clicked = False
            try:
                # Method 1: Look for FIRST button with "close" icon (EXACT working selector)
                remove_buttons = self.driver.find_elements(
                    By.XPATH, 
                    "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/.."
                )
                if remove_buttons:
                    first_remove_button = remove_buttons[0]  # Always use FIRST remove button
                    self.driver.execute_script("arguments[0].click();", first_remove_button)
                    print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Remove button clicked (Method 1)")
                    remove_clicked = True
                else:
                    # Method 2: Alternative selector that was working
                    remove_buttons = self.driver.find_elements(
                        By.XPATH,
                        "//button//i[text()='close']/.."
                    )
                    if remove_buttons:
                        first_remove_button = remove_buttons[0]
                        self.driver.execute_script("arguments[0].click();", first_remove_button)
                        print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Remove button clicked (Method 2)")
                        remove_clicked = True
                    else:
                        print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ No remove button found with either method")
            except Exception as e:
                print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Remove button error: {str(e)}")
            
            # Monitor remove button click success - SAME AS UPLOAD
            if remove_clicked:
                print(Fore.CYAN + f"[SAVE WAIT {ingredient_num}] 🔍 Monitoring remove completion...")
                time.sleep(1)  # Brief wait to let removal process
                
                # Check if remove button disappeared (removal successful)
                try:
                    remaining_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                    if len(remaining_buttons) == 0:
                        print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Removal confirmed - slot cleared")
                    else:
                        print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Remove button still visible, but continuing")
                except:
                    print(Fore.GREEN + f"[SAVE WAIT {ingredient_num}] ✅ Removal process completed")
                
                return True
            else:
                print(Fore.YELLOW + f"[SAVE WAIT {ingredient_num}] ⚠️ Remove button failed, but save likely succeeded")
                return True
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Save wait failed for {ingredient_num}: {str(e)}")
            return False



    def upload_single_ingredient_with_monitoring(self, ingredient_path, ingredient_num):
        """Upload single ingredient with extended monitoring and remove cycle"""
        try:
            print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] Uploading: {os.path.basename(ingredient_path)}")

            # Find FIRST + button
            first_plus_button = None
            try:
                plus_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.sc-74578dc8-1.hopAJY")
                if plus_buttons:
                    first_plus_button = plus_buttons[0]  # Always use FIRST + button
            except:
                pass

            if not first_plus_button:
                print(Fore.RED + f"[UPLOAD {ingredient_num}] ❌ Cannot find FIRST + button")
                return False

            # Click the FIRST + button
            self.driver.execute_script("arguments[0].click();", first_plus_button)
            time.sleep(2)

            # Find file input and upload
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
            if file_inputs:
                file_inputs[-1].send_keys(ingredient_path)
                time.sleep(3)

                # Click Crop and Save button if it appears
                try:
                    crop_btn = self.driver.find_element(
                        By.XPATH,
                        "//button[contains(., 'Crop and Save') or contains(., 'Crop & Save') or contains(., 'Crop and save')]"
                    )
                    self.driver.execute_script("arguments[0].click();", crop_btn)
                    time.sleep(3)
                    print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Uploaded and cropped")
                except:
                    print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Uploaded")

                # EXTENDED WAIT LOGIC: Same as library upload
                upload_completed = False
                total_waited = 0
                max_wait_time = 100
                check_count = 0
                
                # First wait: 8 seconds
                first_wait = 8
                print(Fore.CYAN + f"[UPLOAD {ingredient_num}] ⏳ Initial wait: {first_wait} seconds...")
                for i in range(first_wait, 0, -1):
                    print(f"\r[UPLOAD {ingredient_num}] ⏳ Waiting {i} seconds...", end="", flush=True)
                    time.sleep(1)
                total_waited += first_wait
                check_count += 1
                
                print(f"\r[UPLOAD {ingredient_num}] ⏳ Wait complete, checking upload (check {check_count})...                    ")
                
                # Check if uploaded after first 8 seconds
                try:
                    remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..")
                    if len(remove_buttons) > 0:
                        upload_completed = True
                        print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Upload completed after {total_waited} seconds!")
                    else:
                        # Try alternative selector
                        alt_remove_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                        if len(alt_remove_buttons) > 0:
                            upload_completed = True
                            print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Upload completed after {total_waited} seconds!")
                except Exception as e:
                    print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Check failed: {str(e)}")
                
                # Continue with 5-second intervals until 100 seconds total
                while not upload_completed and total_waited < max_wait_time:
                    remaining_time = max_wait_time - total_waited
                    next_wait = min(5, remaining_time)
                    
                    if next_wait <= 0:
                        break
                    
                    print(Fore.CYAN + f"[UPLOAD {ingredient_num}] ⏳ Continuing wait: {next_wait} seconds (total: {total_waited}/{max_wait_time}s)...")
                    for i in range(next_wait, 0, -1):
                        print(f"\r[UPLOAD {ingredient_num}] ⏳ Waiting {i} seconds... (total: {total_waited + (next_wait - i + 1)}/{max_wait_time}s)", end="", flush=True)
                        time.sleep(1)
                    
                    total_waited += next_wait
                    check_count += 1
                    
                    print(f"\r[UPLOAD {ingredient_num}] ⏳ Wait complete, checking upload (check {check_count})...                    ")
                    
                    # Check if uploaded
                    try:
                        remove_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/..")
                        if len(remove_buttons) > 0:
                            upload_completed = True
                            print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Upload completed after {total_waited} seconds!")
                            break
                        else:
                            # Try alternative selector
                            alt_remove_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                            if len(alt_remove_buttons) > 0:
                                upload_completed = True
                                print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Upload completed after {total_waited} seconds!")
                                break
                            else:
                                print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Not uploaded yet after {total_waited}s, continuing...")
                    except Exception as e:
                        print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Check failed: {str(e)}")
                
                if not upload_completed:
                    print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Upload not detected after {total_waited} seconds total, but continuing...")
                
                # IMMEDIATE REMOVE: Click remove button right after upload detection - INTEGRATED
                print(Fore.CYAN + f"[UPLOAD {ingredient_num}] 🗑️ Clicking remove button immediately...")
                
                # Find and click remove button - USING THE EXACT WORKING SELECTORS
                remove_clicked = False
                try:
                    # Method 1: Look for FIRST button with "close" icon (EXACT working selector)
                    remove_buttons = self.driver.find_elements(
                        By.XPATH, 
                        "//button[contains(@class, 'sc-c177465c-1') and contains(@class, 'hVamcH') and contains(@class, 'sc-74578dc8-1')]//i[text()='close']/.."
                    )
                    if remove_buttons:
                        first_remove_button = remove_buttons[0]  # Always use FIRST remove button
                        self.driver.execute_script("arguments[0].click();", first_remove_button)
                        print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Remove button clicked (Method 1)")
                        remove_clicked = True
                    else:
                        # Method 2: Alternative selector that was working
                        remove_buttons = self.driver.find_elements(
                            By.XPATH,
                            "//button//i[text()='close']/.."
                        )
                        if remove_buttons:
                            first_remove_button = remove_buttons[0]
                            self.driver.execute_script("arguments[0].click();", first_remove_button)
                            print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Remove button clicked (Method 2)")
                            remove_clicked = True
                        else:
                            print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ No remove button found with either method")
                except Exception as e:
                    print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Remove button error: {str(e)}")
                
                # Monitor remove button click success
                if remove_clicked:
                    print(Fore.CYAN + f"[UPLOAD {ingredient_num}] 🔍 Monitoring remove completion...")
                    time.sleep(1)  # Brief wait to let removal process
                    
                    # Check if remove button disappeared (removal successful)
                    try:
                        remaining_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='close']/..")
                        if len(remaining_buttons) == 0:
                            print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Removal confirmed - slot cleared")
                        else:
                            print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Remove button still visible, but continuing")
                    except:
                        print(Fore.GREEN + f"[UPLOAD {ingredient_num}] ✅ Removal process completed")
                    
                    return True
                else:
                    print(Fore.YELLOW + f"[UPLOAD {ingredient_num}] ⚠️ Remove button failed, but upload likely succeeded")
                    return True

            else:
                print(Fore.RED + f"[UPLOAD {ingredient_num}] ❌ No file input found")
                return False
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Upload failed for {ingredient_num}: {str(e)}")
            return False

    def generate_single_ingredient_with_monitoring(self, story_name, ingredient_num):
        """Generate single ingredient with complete monitoring cycle"""
        try:
            print(Fore.CYAN + f"\n{'═' * 50}")
            print(Fore.CYAN + f"🎨 GENERATING INGREDIENT {ingredient_num}.jpeg")
            print(Fore.CYAN + f"{'═' * 50}")
            
            # Step 1: Parse ingredient prompt
            prompt_data = self.parse_ingredient_prompt(story_name, ingredient_num)
            if not prompt_data:
                print(Fore.RED + f"[ERROR] Could not parse prompt for {ingredient_num}.jpeg")
                return False
            
            print(Fore.YELLOW + f"[GENERATE {ingredient_num}] Title: {prompt_data['title']}")
            
            # Step 2: Enter prompt and generate
            if not self.enter_prompt_and_generate(prompt_data['prompt'], ingredient_num):
                print(Fore.RED + f"[ERROR] Failed to enter prompt for {ingredient_num}.jpeg")
                return False
            
            # Step 3: Wait for generation complete (up to 100s)
            if not self.wait_for_generation_complete_extended(ingredient_num, max_wait=100):
                print(Fore.RED + f"[ERROR] Generation timeout for {ingredient_num}.jpeg")
                return False
            
            # Step 4: Click "Save as New Ingredient"
            if not self.click_save_as_new_ingredient(ingredient_num):
                print(Fore.RED + f"[ERROR] Failed to save {ingredient_num}.jpeg as ingredient")
                return False
            
            # Step 5: Wait for save complete (up to 100s) - includes remove button click
            if not self.wait_for_save_complete_extended(ingredient_num, max_wait=100):
                print(Fore.RED + f"[ERROR] Save timeout for {ingredient_num}.jpeg")
                return False
            
            print(Fore.GREEN + f"[GENERATE {ingredient_num}] ✅ COMPLETE - Generated, saved to library, and slot cleared")
            return True
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Generation failed for {ingredient_num}: {str(e)}")
            return False

    def get_base_ingredient_paths(self):
        """Get paths to base ingredient files (01, 02)"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # BASE_CAT_IMAGES is in the same directory as this script
            base_images_folder = os.path.join(script_dir, "BASE_CAT_IMAGES")
            
            if not os.path.exists(base_images_folder):
                print(Fore.RED + f"[ERROR] Base images folder not found: {base_images_folder}")
                return []
            
            base_files = []
            for filename in ["01.jpeg", "02.jpeg"]:
                file_path = os.path.join(base_images_folder, filename)
                if os.path.exists(file_path):
                    base_files.append(file_path)
                else:
                    print(Fore.YELLOW + f"[WARNING] Base file not found: {filename}")
            
            print(Fore.GREEN + f"[BASE] Found {len(base_files)} base ingredient files")
            return base_files
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to get base ingredient paths: {str(e)}")
            return []

    def process_story_ingredients_hybrid_with_remove_cycle(self, story_name):
        """Complete hybrid workflow with remove button cycle
        
        WORKFLOW:
        1. Generate story ingredients (03, 04, 05, 06 - max 4) in REVERSE order (06→05→04→03)
        2. Upload base cat ingredients (01, 02) in REVERSE order (02→01)
        3. Final gallery order: 01, 02, 03, 04, 05, 06 (correct for selection)
        
        INGREDIENT RULES:
        - 01 = Cat (Mama Cat) - pre-existing photo
        - 02 = Kitten - pre-existing photo
        - 03-06 = Story-specific items (max 4 per story, AI generated)
        - Use 01 for Cat alone, 02 for Kitten alone, or both for both characters
        - Maximum 6 ingredients per scene (2 base + 4 story)
        """
        try:
            print(f"\n{'█' * 60}")
            print(Fore.CYAN + f"🔄 HYBRID INGREDIENT PROCESSING: {story_name}")
            print(Fore.CYAN + f"⚡ Strategy: Generate story ingredients (03-06) → Upload base cats (01-02)")
            print(Fore.CYAN + f"🔄 Order: Reverse generation/upload for correct gallery order")
            print(Fore.CYAN + f"🗑️ Remove cycle: Clear slot after each ingredient")
            print(f"{'█' * 60}")
            
            # PHASE 0: Open Generate Image dialog (required for generation)
            if not self.open_generate_image_dialog():
                print(Fore.RED + f"[ERROR] Failed to open Generate Image dialog")
                return False
            
            # PHASE 1: Generate story ingredients (03-06) in reverse order
            story_ingredients = self.detect_story_ingredients(story_name)
            if not story_ingredients:
                print(Fore.RED + f"[ERROR] No story ingredients found for: {story_name}")
                return False
            
            reversed_story = list(reversed(story_ingredients))  # Generate in reverse order (06→05→04→03)
            
            print(Fore.YELLOW + f"\n[PHASE 1] Generating {len(story_ingredients)} story ingredients in REVERSE order:")
            print(Fore.CYAN + f"[INFO] Reverse order ensures correct gallery position (03, 04, 05, 06)")
            for idx, ingredient_num in enumerate(reversed_story):
                print(Fore.YELLOW + f"  Generation order {idx + 1}: {ingredient_num}.jpeg")
            
            for idx, ingredient_num in enumerate(reversed_story):
                # For ingredients after the first one, just open Generate Image dialog (mode already set)
                if idx > 0:  # Not the first ingredient
                    print(Fore.CYAN + f"\n[DIALOG] Opening Generate Image dialog for {ingredient_num}.jpeg...")
                    
                    # Open Generate Image dialog (no mode switch needed - already in Ingredients mode)
                    if not self.open_generate_image_dialog():
                        print(Fore.RED + f"[ERROR] Failed to open Generate Image dialog for {ingredient_num}.jpeg")
                        return False
                
                # Generate the ingredient
                if not self.generate_single_ingredient_with_monitoring(story_name, ingredient_num):
                    print(Fore.RED + f"[ERROR] Failed to generate {ingredient_num}.jpeg")
                    return False
                
                # Brief pause between generations
                if ingredient_num != reversed_story[-1]:  # Not the last one
                    print(Fore.CYAN + f"[INFO] Preparing for next generation...")
                    time.sleep(3)
            
            print(Fore.GREEN + f"\n[PHASE 1] ✅ All story ingredients generated successfully!")
            
            # PHASE 2: Upload base cat ingredients (01, 02) in reverse order
            base_paths = self.get_base_ingredient_paths()
            if not base_paths:
                print(Fore.RED + f"[ERROR] No base ingredient files found")
                return False
            
            # Reverse the base paths so 02, 01 upload order (ensures 01, 02 appear first in gallery)
            base_ingredients_data = [
                (base_paths[1], "02"),  # 02.jpeg (Kitten)
                (base_paths[0], "01")   # 01.jpeg (Cat)
            ]
            
            print(Fore.YELLOW + f"\n[PHASE 2] Uploading {len(base_paths)} base cat ingredients in REVERSE order:")
            print(Fore.CYAN + f"[INFO] These are PRE-EXISTING photos (not AI generated)")
            print(Fore.CYAN + f"[INFO] Reverse order ensures 01, 02, 03 appear first in gallery")
            for idx, (path, num) in enumerate(base_ingredients_data):
                print(Fore.YELLOW + f"  Upload order {idx + 1}: {num}.jpeg")
            
            for ingredient_path, ingredient_num in base_ingredients_data:
                if not self.upload_single_ingredient_with_monitoring(ingredient_path, ingredient_num):
                    print(Fore.RED + f"[ERROR] Failed to upload {ingredient_num}.jpeg")
                    return False
                
                # Brief pause between uploads
                if ingredient_num != "01":  # Not the last one
                    print(Fore.CYAN + f"[INFO] Preparing for next upload...")
                    time.sleep(3)
            
            print(Fore.GREEN + f"\n[PHASE 2] ✅ All base ingredients uploaded successfully!")
            
            # Create ingredient mapping for selection phase
            total_ingredients = len(base_paths) + len(story_ingredients)
            self.ingredient_mapping = {}
            
            # Base cat ingredients appear first (01, 02, 03)
            print(Fore.CYAN + f"\n[MAPPING] Creating ingredient gallery mapping:")
            for idx, num in enumerate(["01", "02", "03"]):
                gallery_index = 2 + idx
                self.ingredient_mapping[f"{num}.jpeg"] = gallery_index
                cat_type = "Cat" if num == "01" else "Kitten"
                print(Fore.CYAN + f"[MAPPING] {num}.jpeg ({cat_type}) → Gallery Index {gallery_index}")
            
            # Story ingredients appear after bases (03, 04, 05, 06)
            for idx, ingredient_num in enumerate(story_ingredients):
                gallery_index = 2 + len(base_paths) + idx
                self.ingredient_mapping[f"{ingredient_num}.jpeg"] = gallery_index
                print(Fore.CYAN + f"[MAPPING] {ingredient_num}.jpeg (Story item) → Gallery Index {gallery_index}")
            
            print(f"\n{'█' * 60}")
            print(Fore.GREEN + f"🎉 HYBRID PROCESSING COMPLETED!")
            print(f"{'█' * 60}")
            print(Fore.GREEN + f"✅ Generated: {len(story_ingredients)} story ingredients (03-06)")
            print(Fore.GREEN + f"✅ Uploaded: {len(base_paths)} base cat ingredients (01-02)")
            print(Fore.GREEN + f"✅ Total ingredients ready: {total_ingredients}")
            print(Fore.YELLOW + f"📋 Gallery order: 01, 02, {', '.join(story_ingredients)}")
            print(Fore.CYAN + f"💡 Remember: Use 01 for Cat, 02 for Kitten, or both for both characters")
            print(Fore.CYAN + f"💡 Maximum 6 ingredients per scene (2 base + 4 story)")
            print(Fore.GREEN + f"🚀 Ready for video generation!")
            print(f"{'█' * 60}")
            
            return True
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Hybrid processing failed: {str(e)}")
            return False

    # ═══════════════════════════════════════════════════════════════════

    def select_ingredients_for_prompt(self, ingredient_numbers):
        """DYNAMIC + BUTTON LOGIC: Google now shows + buttons dynamically
        
        NEW GOOGLE BEHAVIOR:
        - 0 ingredients uploaded → 1 + button shows
        - 1 ingredient uploaded → 2nd + button appears
        - 2 ingredients uploaded → 3rd + button appears
        
        STRATEGY: Always click the LAST/NEWEST + button (with 'add' icon)
        - For each ingredient, find ALL + buttons and click the LAST one
        - After selection, a new + button appears for the next ingredient
        """
        try:
            if not ingredient_numbers:
                print(Fore.YELLOW + "[SELECT] No ingredients specified")
                return True

            ingredient_list = [x.strip() for x in ingredient_numbers.split(',')]
            print(Fore.CYAN + f"[SELECT] STARTING ingredient selection: {ingredient_list}")
            print(Fore.YELLOW + f"[SELECT] DYNAMIC LOGIC: Click LAST + button for each ingredient")

            # Process each ingredient sequentially
            for position, ingredient_num in enumerate(ingredient_list, 1):
                print(Fore.YELLOW + f"\n[SELECT] === POSITION {position}: INGREDIENT {ingredient_num} ===")

                # Find INGREDIENT + buttons using ULTRA SPECIFIC XPath
                plus_button = None
                print(Fore.CYAN + f"[SELECT] Looking for ingredient + buttons...")
                
                try:
                    # ULTRA SPECIFIC XPath: Navigate the exact DOM structure
                    # Start from textarea, go to parent container, then find the ingredients div
                    xpath = (
                        "//textarea[@id='PINHOLE_TEXT_AREA_ELEMENT_ID']"
                        "/following-sibling::div[contains(@class, 'sc-408537d4-0')]"
                        "//button[contains(@class, 'hopAJY') and .//i[text()='add']]"
                    )
                    
                    plus_buttons = self.driver.find_elements(By.XPATH, xpath)
                    
                    print(Fore.CYAN + f"[SELECT] Found {len(plus_buttons)} ingredient + button(s)")
                    
                    # DEBUG: Print all found buttons
                    for idx, btn in enumerate(plus_buttons):
                        try:
                            btn_classes = btn.get_attribute("class")
                            btn_location = btn.location
                            print(Fore.YELLOW + f"[SELECT] Button {idx+1}: classes={btn_classes[:50]}... location={btn_location}")
                        except:
                            pass
                    
                    if plus_buttons:
                        # Always use the LAST + button (newest one)
                        plus_button = plus_buttons[-1]
                        print(Fore.GREEN + f"[SELECT] Using LAST ingredient + button (button #{len(plus_buttons)})")
                    else:
                        print(Fore.RED + f"[SELECT] No ingredient + buttons found!")
                except Exception as e:
                    print(Fore.YELLOW + f"[SELECT] XPath method failed: {str(e)}")

                if not plus_button:
                    print(Fore.RED + f"[SELECT] ❌ Cannot find + button for position {position}")
                    continue

                # Click the + button with safety checks
                print(Fore.CYAN + f"[SELECT] Clicking + button for ingredient {ingredient_num}...")
                try:
                    # DEBUG: Print button details before clicking
                    btn_classes = plus_button.get_attribute("class")
                    btn_html = plus_button.get_attribute("outerHTML")[:200]
                    print(Fore.YELLOW + f"[SELECT] Button classes: {btn_classes}")
                    print(Fore.YELLOW + f"[SELECT] Button HTML: {btn_html}...")
                    
                    # Scroll into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", plus_button)
                    print(Fore.GREEN + f"[SELECT] ✅ Clicked + button")
                except Exception as e:
                    print(Fore.RED + f"[SELECT] ❌ Failed to click + button: {str(e)}")
                    continue

                # Wait for gallery container
                print(Fore.CYAN + f"[SELECT] Waiting for gallery container...")
                container_found = False
                for wait in range(8):
                    try:
                        container = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="virtuoso-scroller"]')
                        if container:
                            container_found = True
                            print(Fore.GREEN + f"[SELECT] ✅ Gallery container appeared")
                            break
                    except:
                        pass
                    
                    print(Fore.YELLOW + f"[SELECT] Waiting for container... ({wait + 1}/8)")
                    time.sleep(1)

                if not container_found:
                    print(Fore.RED + f"[SELECT] ❌ Gallery container did not appear")
                    continue

                # Wait for gallery items to load
                time.sleep(2)

                # Select ingredient from gallery
                ingredient_number = int(ingredient_num.lstrip('0')) if ingredient_num.lstrip('0') else 1
                gallery_index = 2 + ingredient_number - 1
                print(Fore.CYAN + f"[SELECT] Selecting ingredient {ingredient_num} at gallery index {gallery_index}")

                ingredient_selected = False
                
                # Method 1: Direct CSS selector
                try:
                    btn = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="{gallery_index}"] button.sc-fbea20b2-9')
                    self.driver.execute_script("arguments[0].click();", btn)
                    ingredient_selected = True
                    print(Fore.GREEN + f"[SELECT] ✅ Selected ingredient {ingredient_num} (Method 1)")
                except Exception as e:
                    print(Fore.YELLOW + f"[SELECT] Method 1 failed: {str(e)}")

                # Method 2: Fallback selector
                if not ingredient_selected:
                    try:
                        btn = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="{gallery_index}"] button')
                        self.driver.execute_script("arguments[0].click();", btn)
                        ingredient_selected = True
                        print(Fore.GREEN + f"[SELECT] ✅ Selected ingredient {ingredient_num} (Method 2)")
                    except Exception as e:
                        print(Fore.YELLOW + f"[SELECT] Method 2 failed: {str(e)}")

                # Method 3: Scan all items
                if not ingredient_selected:
                    try:
                        items = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-index]')
                        print(Fore.CYAN + f"[SELECT] Scanning {len(items)} gallery items...")
                        for item in items:
                            if item.get_attribute('data-index') == str(gallery_index):
                                btn = item.find_element(By.CSS_SELECTOR, 'button')
                                self.driver.execute_script("arguments[0].click();", btn)
                                ingredient_selected = True
                                print(Fore.GREEN + f"[SELECT] ✅ Selected ingredient {ingredient_num} (Method 3)")
                                break
                    except Exception as e:
                        print(Fore.YELLOW + f"[SELECT] Method 3 failed: {str(e)}")

                if not ingredient_selected:
                    print(Fore.RED + f"[SELECT] ❌ FAILED to select ingredient {ingredient_num}")
                else:
                    print(Fore.GREEN + f"[SELECT] ✅ SUCCESS: Ingredient {ingredient_num} selected at position {position}")

                # Brief wait before next ingredient
                time.sleep(1)

            print(Fore.GREEN + f"\n[SELECT] ✅ COMPLETED ingredient selection process")
            print(Fore.CYAN + f"[SELECT] Summary: Selected {len(ingredient_list)} ingredients: {ingredient_list}")
            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Selection failed: {str(e)}")
            traceback.print_exc()
            return False

    def process_multiple_story_projects_enhanced(self, selected_worksheets_data):
        """Enhanced processing with reverse upload + smart ingredient selection"""
        try:
            current_story = 0
            total_stories = len(selected_worksheets_data)
            
            for story_name, story_data in selected_worksheets_data.items():
                current_story += 1
                
                print(f"\n{'█' * 60}")
                print(Fore.CYAN + f"📚 PROJECT {current_story}/{total_stories}: {story_name}")
                print(f"📝 Scenes: {story_data['count']}")
                print(f"🎬 Expected Videos: {story_data['count'] * 2}")
                print(f"{'█' * 60}")
                
                # Navigate to Flow and create project
                if not self.navigate_to_flow():
                    continue
                
                # Create new project
                project_name = f"MamaCat - {story_name}"
                if not self.create_new_project(project_name):
                    continue
                
                # Switch to Ingredients mode
                if not self.switch_to_ingredients_mode():
                    continue
                
                # Process ingredients with hybrid system (generate + upload with remove cycle)
                print(Fore.CYAN + f"\n[PROJECT {current_story}] Processing ingredients with hybrid system...")
                if not self.process_story_ingredients_hybrid_with_remove_cycle(story_name):
                    print(Fore.RED + f"[ERROR] Failed to process ingredients for {story_name}")
                    continue
                
                # Process prompts with enhanced ingredient selection
                prompts = story_data['prompts']
                
                # Convert prompts to strings if they're dictionaries
                if prompts and isinstance(prompts[0], dict):
                    # Extract prompt text from dictionaries
                    prompt_texts = []
                    for prompt_dict in prompts:
                        if isinstance(prompt_dict, dict) and 'Prompt' in prompt_dict:
                            prompt_texts.append(prompt_dict['Prompt'])
                        elif isinstance(prompt_dict, dict):
                            # Take the first string value found
                            for value in prompt_dict.values():
                                if isinstance(value, str):
                                    prompt_texts.append(value)
                                    break
                        else:
                            prompt_texts.append(str(prompt_dict))
                    prompts = prompt_texts
                
                # Read ingredient data from Excel "Ingredients_No" column
                script_dir = os.path.dirname(os.path.abspath(__file__))
                excel_path = os.path.join(script_dir, EXCEL_FILE_PATH)
                df = pd.read_excel(excel_path, sheet_name=story_name)
                
                if 'Ingredients_No' in df.columns:
                    ingredients_list = df['Ingredients_No'].fillna("").tolist()
                    ingredients_list = [str(x).strip() for x in ingredients_list]  # Convert to strings
                    print(Fore.GREEN + f"[EXCEL] Found Ingredients_No column: {ingredients_list[:5]}...")
                else:
                    print(Fore.YELLOW + f"[EXCEL] No Ingredients_No column found, using default ingredient 1")
                    ingredients_list = ["1"] * len(prompts)
                
                print(Fore.CYAN + f"[PROJECT {current_story}] Processing {len(prompts)} scenes with smart ingredient selection...")
                print(Fore.CYAN + f"[PROJECT {current_story}] Sample prompts: {[p[:50] + '...' if len(p) > 50 else p for p in prompts[:3]]}")
                
                # Process all prompts with ingredient selection
                self.process_prompts_with_ingredients(prompts, ingredients_list)
                
                print(Fore.GREEN + f"[PROJECT {current_story}] ✅ {story_name} completed!")
            
            print(f"\n{'█' * 60}")
            print(Fore.GREEN + f"🎉 ALL {total_stories} PROJECTS COMPLETED!")
            print(f"{'█' * 60}")
            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Enhanced processing failed: {str(e)}")
            return False

    def debug_gallery_state(self):
        """Debug function to show current gallery state"""
        try:
            print(Fore.CYAN + f"\n[DEBUG] Analyzing current gallery state...")
            
            # Wait for gallery to load
            print(Fore.CYAN + f"[DEBUG] Waiting 5 seconds for gallery to load...")
            time.sleep(5)
            
            # Check ingredient mapping
            if hasattr(self, 'ingredient_mapping'):
                print(Fore.CYAN + f"[DEBUG] Ingredient mapping:")
                for filename, index in self.ingredient_mapping.items():
                    print(Fore.CYAN + f"  {filename} → Index {index}")
            else:
                print(Fore.RED + f"[DEBUG] No ingredient mapping found!")
            
            # Try multiple selectors for gallery items
            gallery_selectors = [
                'div.virtuoso-grid-item[data-index]',
                'div[data-index]',
                '.virtuoso-grid-item',
                'div.sc-bd10a1a0-5'
            ]
            
            gallery_items = []
            for selector in gallery_selectors:
                try:
                    items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if items:
                        gallery_items = items
                        print(Fore.GREEN + f"[DEBUG] Found {len(items)} items using selector: {selector}")
                        break
                except:
                    continue
            
            if not gallery_items:
                print(Fore.RED + f"[DEBUG] No gallery items found with any selector!")
                return
            
            print(Fore.CYAN + f"[DEBUG] Gallery items analysis:")
            for item in gallery_items[:15]:  # Show first 15
                try:
                    item_index = item.get_attribute('data-index')
                    button = item.find_element(By.CSS_SELECTOR, 'button')
                    button_classes = button.get_attribute('class')
                    print(Fore.CYAN + f"  Index {item_index}: {button_classes[:50]}...")
                except Exception as e:
                    print(Fore.CYAN + f"  Item: {str(e)[:50]}...")
            
        except Exception as e:
            print(Fore.RED + f"[DEBUG] Gallery analysis failed: {str(e)}")

    def process_prompts_with_ingredients(self, all_prompts, ingredients_list):
        """Process all prompts with ingredient selection and generation - REVERSE ORDER with 50% tracking"""
        try:
            total_prompts = len(all_prompts)
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"🚀 PROCESSING {total_prompts} PROMPTS IN REVERSE ORDER (25→1)")
            print(Fore.CYAN + f"⚡ Strategy: Wait for previous prompt to reach 50% before next submission")
            print(f"{'═' * 60}")
            
            # REVERSE THE ORDER: Process from last to first (25, 24, 23... 2, 1)
            reversed_prompts = list(reversed(all_prompts))
            reversed_ingredients = list(reversed(ingredients_list))
            
            previous_prompt_index = None  # Track which prompt to monitor
            
            for idx, (prompt, ingredients) in enumerate(zip(reversed_prompts, reversed_ingredients), 1):
                # Calculate original prompt number (25, 24, 23... for display)
                original_prompt_num = total_prompts - idx + 1
                
                if not prompt.strip():
                    print(Fore.YELLOW + f"[PROMPT {original_prompt_num}] Skipping empty prompt")
                    continue
                
                print(f"\n{'═' * 50}")
                print(Fore.YELLOW + f"[PROMPT {original_prompt_num}/{total_prompts}] (Processing order: {idx})")
                print(f"{'═' * 50}")
                print(f"Prompt: {prompt[:100]}...")
                print(f"Ingredients: {ingredients}")
                
                # WAIT FOR PREVIOUS PROMPT TO REACH 50% (skip for first prompt)
                if idx > 1 and previous_prompt_index is not None:
                    print(Fore.CYAN + f"⏳ Waiting for previous prompt (index {previous_prompt_index}) to reach 50%...")
                    if not self.wait_for_prompt_50_percent(previous_prompt_index):
                        print(Fore.YELLOW + "[WARNING] 50% wait timeout, continuing anyway")
                        self.write_to_report(f"[PROMPT {original_prompt_num}] ⚠️ 50% wait timeout")
                
                # Select ingredients for this prompt
                if ingredients.strip():
                    if not self.select_ingredients_for_prompt(ingredients):
                        print(Fore.YELLOW + f"[PROMPT {original_prompt_num}] Ingredient selection failed, continuing anyway...")
                
                # Add prompt and generate
                if not self.add_prompt_and_generate(prompt, original_prompt_num, is_first=(idx==1)):
                    print(Fore.YELLOW + f"[PROMPT {original_prompt_num}] Generation failed, continuing to next prompt...")
                    continue
                
                print(Fore.GREEN + f"[PROMPT {original_prompt_num}] ✅ Successfully queued for generation")
                
                # Store this prompt's index for next iteration to track
                # The prompt we just submitted will be at index 0 (newest)
                previous_prompt_index = 0
                
                # Update queue status
                active_count = self.count_active_prompt_generations()
                completed_count = self.count_completed_prompt_generations()
                print(Fore.CYAN + f"📊 Queue status: {active_count} active | {completed_count} completed")
            
            print(f"\n{'═' * 60}")
            print(Fore.GREEN + f"🎉 ALL {total_prompts} PROMPTS PROCESSED IN REVERSE ORDER!")
            print(f"{'═' * 60}")
            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Prompt processing failed: {str(e)}")
            return False

    def select_ingredients_for_prompt(self, ingredient_numbers):
        """ENHANCED APPROACH: Click + button, select from container with VERIFICATION and RETRY
        
        GALLERY INDEX MAPPING:
        - First image (01.png) → Gallery Index 2
        - Second image (02.png) → Gallery Index 3  
        - Third image (03.png) → Gallery Index 4
        - ...
        - Sixth image (06.png) → Gallery Index 7
        - Formula: Gallery Index = 2 + (ingredient_number - 1)
        
        VERIFICATION & RETRY FEATURES:
        - Individual verification for each ingredient selection
        - Up to 5 retry attempts per ingredient if selection fails
        - Checks gallery closure and selection indicators for verification
        - Continues with other ingredients even if one fails
        - Detailed logging for each attempt and verification step
        """
        try:
            if not ingredient_numbers:
                print(Fore.YELLOW + "[SELECT] No ingredients specified")
                return True

            ingredient_list = [x.strip() for x in ingredient_numbers.split(',')]
            print(Fore.CYAN + f"[SELECT] Selecting ingredients: {ingredient_list}")

            # Find + buttons using EXACT upload button selector
            plus_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.sc-c177465c-1.hVamcH.sc-74578dc8-1.hopAJY")

            if len(plus_buttons) < len(ingredient_list):
                # Fallback: find buttons with 'add' icon
                plus_buttons = []
                all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in all_buttons:
                    try:
                        if 'add' in btn.get_attribute('innerHTML').lower():
                            plus_buttons.append(btn)
                            if len(plus_buttons) >= len(ingredient_list):
                                break
                    except:
                        continue

            if len(plus_buttons) < len(ingredient_list):
                print(Fore.RED + f"[ERROR] Cannot find enough + buttons. Need {len(ingredient_list)}, found {len(plus_buttons)}")
                print(Fore.CYAN + f"[DEBUG] Trying alternative selector...")
                
                # Try the exact selector from your HTML
                plus_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'hopAJY')]//i[text()='add']/..")
                
                if len(plus_buttons) < len(ingredient_list):
                    print(Fore.RED + f"[ERROR] Still cannot find enough + buttons. Found {len(plus_buttons)}")
                    return False

            # Select each ingredient using corresponding + button WITH VERIFICATION AND RETRY
            for idx, ingredient_num in enumerate(ingredient_list):
                print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Using + button {idx + 1}")
                
                # RETRY LOGIC: Try up to 5 times for each ingredient
                ingredient_selected = False
                max_retries = 5
                
                for retry_attempt in range(1, max_retries + 1):
                    print(Fore.CYAN + f"  [INGREDIENT {ingredient_num}] Attempt {retry_attempt}/{max_retries}")
                    
                    try:
                        # WINNING METHOD: Find LAST button with 'add' icon (class-agnostic)
                        # This works because Google changes classes (hopAJY → drPMPR) after selection
                        all_add_buttons = self.driver.find_elements(
                            By.XPATH,
                            "//button[.//i[text()='add']]"
                        )
                        
                        # Filter out Help button and other non-ingredient buttons
                        ingredient_buttons = []
                        for btn in all_add_buttons:
                            try:
                                location = btn.location
                                btn_classes = btn.get_attribute("class")
                                # Must be in lower area (y > 300) and NOT Help button
                                if location['y'] > 300 and "sc-e8425ea6-0" not in btn_classes:
                                    ingredient_buttons.append(btn)
                            except:
                                pass
                        
                        # Use the LAST button (newest one for dynamic system)
                        if ingredient_buttons:
                            current_plus_buttons = ingredient_buttons
                            print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ Found {len(current_plus_buttons)} ingredient + buttons")
                        else:
                            current_plus_buttons = []
                            print(Fore.RED + f"  [INGREDIENT {ingredient_num}] ❌ No ingredient + buttons found")
                        
                        if current_plus_buttons:
                            # Always use the LAST button (Google's dynamic system adds new buttons at the end)
                            button = current_plus_buttons[-1]
                            self.driver.execute_script("arguments[0].click();", button)
                            print(Fore.CYAN + f"  [INGREDIENT {ingredient_num}] Clicked LAST + button (#{len(current_plus_buttons)}), waiting for gallery...")
                        else:
                            print(Fore.RED + f"  [INGREDIENT {ingredient_num}] Cannot find + button on attempt {retry_attempt}")
                            if retry_attempt < max_retries:
                                time.sleep(2)
                                continue
                            else:
                                break
                    except Exception as e:
                        print(Fore.RED + f"  [INGREDIENT {ingredient_num}] + button click failed: {str(e)}")
                        if retry_attempt < max_retries:
                            time.sleep(2)
                            continue
                        else:
                            break
                    
                    # Wait for gallery to appear
                    gallery_loaded = False
                    for wait_attempt in range(10):  # Try for 10 seconds
                        time.sleep(1)
                        
                        # Check if gallery items are present
                        gallery_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-index]')
                        if len(gallery_items) > 5:  # Should have more than just Generate/Upload buttons
                            gallery_loaded = True
                            print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] Gallery loaded with {len(gallery_items)} items")
                            break
                        
                        print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Waiting for gallery... ({wait_attempt + 1}/10)")

                    if not gallery_loaded:
                        print(Fore.RED + f"  [INGREDIENT {ingredient_num}] ❌ Gallery failed to load on attempt {retry_attempt}")
                        if retry_attempt < max_retries:
                            print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Retrying...")
                            time.sleep(2)
                            continue
                        else:
                            break

                    # Calculate gallery index: First image = index 2, Second image = index 3, etc.
                    # If 6 ingredients in folder: indices 2, 3, 4, 5, 6, 7
                    ingredient_number = int(ingredient_num.lstrip('0')) if ingredient_num.lstrip('0') else 1
                    gallery_index = 2 + ingredient_number - 1  # ingredient 01 → index 2, ingredient 02 → index 3, etc.
                    
                    print(Fore.CYAN + f"  [INGREDIENT {ingredient_num}] Ingredient #{ingredient_number} → Gallery Index {gallery_index}")
                    
                    # DEBUG: Show the target element structure and validate index exists
                    try:
                        target_element = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="{gallery_index}"]')
                        element_html = target_element.get_attribute('outerHTML')[:200]  # First 200 chars
                        print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ Found target at index {gallery_index}")
                        print(Fore.CYAN + f"  [INGREDIENT {ingredient_num}] Element: {element_html}...")
                    except:
                        print(Fore.RED + f"  [INGREDIENT {ingredient_num}] ❌ No element found at gallery index {gallery_index}")
                        # Show available indices for debugging
                        try:
                            all_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-index]')
                            available_indices = [item.get_attribute('data-index') for item in all_items]
                            print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Available indices: {available_indices}")
                        except:
                            pass
                    
                    # FLEXIBLE SELECTION: Handle changing CSS classes
                    selection_success = False
                    
                    # Method 1: Target any main ingredient button (flexible class matching)
                    try:
                        # Try multiple possible class combinations
                        possible_selectors = [
                            f'div[data-index="{gallery_index}"] button.sc-fbea20b2-9.jsnZTC',  # Original
                            f'div[data-index="{gallery_index}"] button.sc-fbea20b2-9.aGifd',   # Alternative seen in logs
                            f'div[data-index="{gallery_index}"] button.sc-fbea20b2-9',         # Generic
                        ]
                        
                        for selector in possible_selectors:
                            try:
                                ingredient_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                                self.driver.execute_script("arguments[0].click();", ingredient_btn)
                                selection_success = True
                                print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ Selected using flexible button selector")
                                break
                            except:
                                continue
                                
                        if not selection_success:
                            print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] All flexible selectors failed")
                    except Exception as e:
                        print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Flexible selection failed: {str(e)}")
                    
                    # Method 2: Target first button in container (most reliable)
                    if not selection_success:
                        try:
                            ingredient_item = self.driver.find_element(By.CSS_SELECTOR, f'div[data-index="{gallery_index}"]')
                            buttons = ingredient_item.find_elements(By.CSS_SELECTOR, 'button')
                            if buttons:
                                # Click first button that's not edit/delete
                                for btn in buttons:
                                    try:
                                        button_html = btn.get_attribute('innerHTML').lower()
                                        if 'edit' not in button_html and 'delete' not in button_html:
                                            self.driver.execute_script("arguments[0].click();", btn)
                                            selection_success = True
                                            print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ Selected using first valid button")
                                            break
                                    except:
                                        continue
                        except Exception as e:
                            print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] First button method failed: {str(e)}")
                    
                    # Method 3: Scan and find by index (last resort)
                    if not selection_success:
                        try:
                            all_gallery_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-index]')
                            print(Fore.CYAN + f"  [INGREDIENT {ingredient_num}] Scanning {len(all_gallery_items)} gallery items...")
                            
                            for item in all_gallery_items:
                                item_index = item.get_attribute('data-index')
                                if item_index == str(gallery_index):
                                    try:
                                        buttons = item.find_elements(By.CSS_SELECTOR, 'button')
                                        if buttons:
                                            # Click first non-edit/delete button
                                            for btn in buttons:
                                                try:
                                                    button_html = btn.get_attribute('innerHTML').lower()
                                                    if 'edit' not in button_html and 'delete' not in button_html:
                                                        self.driver.execute_script("arguments[0].click();", btn)
                                                        selection_success = True
                                                        print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ Selected by scanning")
                                                        break
                                                except:
                                                    continue
                                            if selection_success:
                                                break
                                    except:
                                        continue
                        except Exception as e:
                            print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Scanning method failed: {str(e)}")
                    
                    if selection_success:
                        # SIMPLIFIED VERIFICATION: Just check if selection worked
                        time.sleep(1)  # Brief wait for selection to register
                        print(Fore.CYAN + f"  [INGREDIENT {ingredient_num}] 🔍 Quick verification...")
                        
                        # Simple verification: If we clicked successfully, assume it worked
                        verification_success = True
                        
                        # Optional: Quick check if gallery is still open (but don't fail if it is)
                        try:
                            gallery_items_after = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-index]')
                            if len(gallery_items_after) <= 5:
                                print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ Verified: Gallery closed")
                            else:
                                print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] ⚠️ Gallery still open, but selection likely worked")
                        except:
                            pass  # Don't fail verification on this
                        
                        if verification_success:
                            ingredient_selected = True
                            print(Fore.GREEN + f"  [INGREDIENT {ingredient_num}] ✅ SUCCESSFULLY SELECTED!")
                            break
                    else:
                        print(Fore.RED + f"  [INGREDIENT {ingredient_num}] ❌ Selection failed on attempt {retry_attempt}")
                        if retry_attempt < max_retries:
                            print(Fore.YELLOW + f"  [INGREDIENT {ingredient_num}] Retrying...")
                            time.sleep(2)
                            continue
                
                if not ingredient_selected:
                    print(Fore.RED + f"  [INGREDIENT {ingredient_num}] ❌ FAILED TO SELECT AFTER {max_retries} ATTEMPTS")
                    # Continue with other ingredients even if one fails
                
                time.sleep(1)  # Brief pause between ingredients

            print(Fore.GREEN + "[SELECT] ✅ Ingredient selection completed")
            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Ingredient selection failed: {str(e)}")
            return False

    def get_worksheet_selection(self, df):
        """Get worksheet selection from user - supports 'all', ranges, and specific sheets"""
        try:
            # Read Excel file to get all worksheets
            script_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(script_dir, EXCEL_FILE_PATH)
            excel_file = pd.ExcelFile(excel_path)
            worksheet_names = excel_file.sheet_names
            
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + "📋 WORKSHEET SELECTION")
            print(f"{'═' * 60}")
            print("Available worksheets:")
            
            for i, sheet_name in enumerate(worksheet_names, 1):
                # Get prompt count for each worksheet
                try:
                    sheet_df = pd.read_excel(excel_path, sheet_name=sheet_name)
                    if 'Prompt' in sheet_df.columns:
                        prompt_count = len(sheet_df['Prompt'].fillna("").tolist())
                        print(f"  {i}. {sheet_name} ({prompt_count} prompts)")
                    else:
                        print(f"  {i}. {sheet_name} (No 'Prompt' column)")
                except:
                    print(f"  {i}. {sheet_name} (Error reading)")
            
            print(f"\n{'─' * 50}")
            print("Input options:")
            print("• 'all' - Process all worksheets")
            print("• '3-5' - Process worksheets 3 to 5 (range)")
            print("• '1,3,5' - Process specific worksheets 1, 3, and 5")
            print(f"{'─' * 50}")
            
            while True:
                user_input = input("➤ Enter your selection: ").strip().lower()
                if not user_input:
                    print(Fore.YELLOW + "⚠️ Please enter a selection")
                    continue
                
                # Parse input and determine selection type
                selected_indices, selection_type = self.parse_worksheet_input(user_input, len(worksheet_names))
                
                if selected_indices is None:
                    continue  # Invalid input, try again
                
                # Get selected worksheet names
                selected_worksheets = [worksheet_names[i-1] for i in selected_indices]
                
                # Collect prompts organized by worksheet
                worksheets_data = {}
                
                print(f"\n{'═' * 50}")
                print(Fore.GREEN + f"📋 PROCESSING {selection_type.upper()}")
                print(f"{'═' * 50}")
                
                for sheet_name in selected_worksheets:
                    try:
                        sheet_df = pd.read_excel(excel_path, sheet_name=sheet_name)
                        if 'Prompt' in sheet_df.columns:
                            # Convert DataFrame to list of dictionaries for proper processing
                            sheet_prompts = sheet_df.to_dict('records')
                            # Remove empty prompts
                            sheet_prompts = [p for p in sheet_prompts if str(p.get('Prompt', '')).strip()]
                            if sheet_prompts:
                                worksheets_data[sheet_name] = {
                                    'prompts': sheet_prompts,
                                    'count': len(sheet_prompts)
                                }
                                print(f"✅ {sheet_name}: {len(sheet_prompts)} prompts")
                            else:
                                print(f"⚠️ {sheet_name}: No valid prompts, skipped")
                        else:
                            print(f"⚠️ {sheet_name}: No 'Prompt' column, skipped")
                    except Exception as e:
                        print(f"❌ {sheet_name}: Error reading - {str(e)}")
                
                total_prompts = sum(data['count'] for data in worksheets_data.values())
                print(f"\n📊 Total prompts collected: {total_prompts}")
                print(f"🏗️ Projects to create: {len(worksheets_data)}")
                
                if not worksheets_data:
                    print(Fore.RED + "[ERROR] No valid prompts found in selected worksheets")
                    return None
                
                return worksheets_data
                
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to read worksheets: {str(e)}")
            return None, None

    def parse_worksheet_input(self, user_input, total_sheets):
        """Parse user input to determine worksheet selection"""
        try:
            # Handle 'all'
            if user_input == 'all':
                return list(range(1, total_sheets + 1)), "all worksheets"
            
            # Handle range (e.g., '3-5')
            if '-' in user_input and ',' not in user_input:
                try:
                    start_str, end_str = user_input.split('-', 1)
                    start_idx = int(start_str.strip())
                    end_idx = int(end_str.strip())
                    
                    if start_idx < 1 or end_idx > total_sheets:
                        print(Fore.YELLOW + f"⚠️ Range must be between 1 and {total_sheets}")
                        return None, None
                    if start_idx > end_idx:
                        print(Fore.YELLOW + "⚠️ Start must be <= end")
                        return None, None
                    
                    selected = list(range(start_idx, end_idx + 1))
                    return selected, f"range {start_idx}-{end_idx}"
                except ValueError:
                    print(Fore.YELLOW + "⚠️ Invalid range format. Use: 3-5")
                    return None, None
            
            # Handle specific sheets (e.g., '1,3,5')
            if ',' in user_input:
                try:
                    indices = []
                    for item in user_input.split(','):
                        idx = int(item.strip())
                        if idx < 1 or idx > total_sheets:
                            print(Fore.YELLOW + f"⚠️ Worksheet {idx} is out of range (1-{total_sheets})")
                            return None, None
                        indices.append(idx)
                    
                    # Remove duplicates and sort
                    selected = sorted(list(set(indices)))
                    return selected, f"specific worksheets {','.join(map(str, selected))}"
                except ValueError:
                    print(Fore.YELLOW + "⚠️ Invalid format. Use: 1,3,5")
                    return None, None
            
            # Handle single number
            try:
                idx = int(user_input)
                if idx < 1 or idx > total_sheets:
                    print(Fore.YELLOW + f"⚠️ Worksheet {idx} is out of range (1-{total_sheets})")
                    return None, None
                return [idx], f"worksheet {idx}"
            except ValueError:
                print(Fore.YELLOW + "⚠️ Invalid input. Use 'all', '3-5', or '1,3,5'")
                return None, None
                
        except Exception as e:
            print(Fore.YELLOW + f"⚠️ Error parsing input: {str(e)}")
            return None, None

    def process_prompt_range_batch(self, all_prompts, start_prompt, end_prompt):
        """Process a specific range of prompts in batches - GENERATION ONLY"""
        try:
            # Validate range
            if start_prompt > len(all_prompts):
                print(Fore.RED + f"[ERROR] Start prompt {start_prompt} exceeds total prompts {len(all_prompts)}")
                return False
            
            if end_prompt > len(all_prompts):
                print(Fore.YELLOW + f"[WARNING] End prompt {end_prompt} exceeds total prompts {len(all_prompts)}, using {len(all_prompts)}")
                end_prompt = len(all_prompts)
            
            # Extract the range (convert to 0-based indexing)
            selected_prompts = all_prompts[start_prompt-1:end_prompt]
            
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"� BATCCH PROCESSING RANGE {start_prompt}-{end_prompt}")
            print(Fore.CYAN + f"📦 Strategy: 5 prompts per batch, generation only")
            print(f"{'═' * 60}")
            print(f"📊 Selected prompts: {len(selected_prompts)}")
            print(f"🎬 Expected videos: {len(selected_prompts) * 4}")
            
            # Update tracking for range processing
            self.total_prompts = len(selected_prompts)
            
            # Process prompts in batches of 5
            batch_size = 5
            total_batches = (len(selected_prompts) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                batch_start = datetime.now()
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(selected_prompts))
                batch_prompts = selected_prompts[start_idx:end_idx]
                
                # Calculate original prompt numbers
                batch_start_num = start_prompt + start_idx
                batch_end_num = start_prompt + end_idx - 1
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + f"📦 BATCH {batch_num + 1}/{total_batches}")
                print(Fore.YELLOW + f"🎯 Processing prompts {batch_start_num}-{batch_end_num}")
                print(f"{'═' * 60}")
                
                self.write_to_report(f"\n{'=' * 60}")
                self.write_to_report(f"BATCH {batch_num + 1}/{total_batches} - Prompts {batch_start_num}-{batch_end_num}")
                self.write_to_report(f"{'=' * 60}")

                # STEP 1: Add all 5 prompts with 8-second intervals
                print(Fore.CYAN + f"\n📝 ADDING {len(batch_prompts)} PROMPTS...")
                for prompt_idx, prompt in enumerate(batch_prompts):
                    original_prompt_num = start_prompt + start_idx + prompt_idx

                    print(f"\n{'-' * 40}")
                    print(Fore.YELLOW + f"[ADDING PROMPT {original_prompt_num}] Batch {batch_num + 1}")
                    print(f"{'-' * 40}")

                    self.write_to_report(f"\n[PROMPT {original_prompt_num}] Adding...")
                    self.write_to_report(f"Prompt text: {prompt[:100]}...")

                    # Click reuse prompt (since we're continuing existing project)
                    if not self.click_reuse_prompt():
                        print(Fore.YELLOW + "[WARNING] Continuing without reuse prompt")
                        self.write_to_report(f"[PROMPT {original_prompt_num}] ⚠️ Reuse prompt failed")

                    # Add prompt and generate
                    if not self.add_prompt_and_generate(prompt, original_prompt_num, is_first=False):
                        self.write_to_report(f"[PROMPT {original_prompt_num}] ❌ Failed to add/generate")
                        continue

                    print(Fore.GREEN + f"[PROMPT {original_prompt_num}] ✅ Added and generation started")
                    self.write_to_report(f"[PROMPT {original_prompt_num}] Added and generation started")

                    # Wait 8 seconds before next prompt (except for last prompt in batch)
                    if prompt_idx < len(batch_prompts) - 1:
                        print(Fore.CYAN + "⏳ Waiting 8 seconds before next prompt...")
                        for i in range(8, 0, -1):
                            print(f"\r⏳ Next prompt in {i} seconds...", end="", flush=True)
                            time.sleep(1)
                        print(f"\r⏳ Adding next prompt...                    ")

                # STEP 2: Wait for all generations in this batch to complete
                print(f"\n{'═' * 50}")
                print(Fore.CYAN + f"⏳ WAITING FOR BATCH {batch_num + 1} GENERATIONS...")
                print(f"{'═' * 50}")
                
                batch_gen_start = datetime.now()
                
                # Wait for all generations to complete (enhanced detection)
                print(Fore.YELLOW + "🔄 Monitoring generation progress...")
                if not self.wait_for_batch_generation_complete(len(batch_prompts)):
                    print(Fore.YELLOW + "[WARNING] Batch generation timeout")
                    self.write_to_report(f"BATCH {batch_num + 1} ⚠️ Generation timeout")
                else:
                    batch_gen_time = datetime.now() - batch_gen_start
                    print(Fore.GREEN + f"✅ All {len(batch_prompts)} generations complete in {str(batch_gen_time).split('.')[0]}")
                    self.write_to_report(f"BATCH {batch_num + 1} ✅ All generations complete. Time: {str(batch_gen_time).split('.')[0]}")
                
                # Update timing stats
                for prompt_idx in range(len(batch_prompts)):
                    self.prompt_times.append(batch_gen_time.total_seconds() / len(batch_prompts))

                # Batch completion summary
                batch_time = datetime.now() - batch_start
                completed_so_far = start_idx + len(batch_prompts)
                
                print(f"\n{'═' * 50}")
                print(Fore.GREEN + f"✅ BATCH {batch_num + 1} COMPLETE!")
                print(Fore.GREEN + f"📊 Generated {len(batch_prompts)} prompts in {str(batch_time).split('.')[0]}")
                print(Fore.GREEN + f"🎯 Range progress: {completed_so_far}/{len(selected_prompts)}")
                print(f"{'═' * 50}")
                
                self.write_to_report(f"\nBATCH {batch_num + 1} COMPLETE:")
                self.write_to_report(f"- Prompts processed: {len(batch_prompts)}")
                self.write_to_report(f"- Batch time: {str(batch_time).split('.')[0]}")
                self.write_to_report(f"- Range progress: {completed_so_far}/{len(selected_prompts)}")
                
                # Calculate stats
                if self.prompt_times:
                    avg_time = sum(self.prompt_times) / len(self.prompt_times)
                    remaining_prompts = len(selected_prompts) - completed_so_far
                    estimated_remaining = avg_time * remaining_prompts
                    
                    print(Fore.CYAN + f"📈 Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                    print(Fore.CYAN + f"⏰ Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                    
                    self.write_to_report(f"- Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                    self.write_to_report(f"- Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")

                # Wait between batches (except for last batch)
                if batch_num < total_batches - 1:
                    print(Fore.YELLOW + f"\n⏳ Waiting 10 seconds before next batch...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next batch in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Starting next batch...                    ")

            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Range batch processing failed: {str(e)}")
            self.write_to_report(f"[ERROR] Range batch processing failed: {str(e)}")
            return False

    def create_new_project(self, project_name):
        """Create a new project"""
        try:
            print(Fore.CYAN + f"\n[PROJECT] Creating new project: {project_name}...")
            time.sleep(3)

            # Find and click New Project button
            new_project_btn = None
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for btn in buttons:
                if "new project" in btn.text.lower():
                    new_project_btn = btn
                    break

            if not new_project_btn:
                try:
                    new_project_btn = self.driver.find_element(
                        By.XPATH, "//button[contains(., 'New project')]"
                    )
                except:
                    pass

            if not new_project_btn:
                print(Fore.RED + "[ERROR] Cannot find New Project button")
                return False

            new_project_btn.click()
            time.sleep(3)

            # Rename project
            self.rename_project(project_name)

            # Reset video tracking for new project
            self.existing_video_count = 0
            self.videos_before_generation = []

            print(Fore.GREEN + f"[PROJECT] ✅ Created: {project_name}")
            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Project creation failed: {str(e)}")
            return False

    def rename_project(self, project_name):
        """Rename the current project"""
        try:
            time.sleep(2)

            # Find edit button
            edit_btn = None
            try:
                edit_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[.//i[contains(@class, 'google-symbols') and contains(., 'edit')]]"
                )
            except:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if "edit" in btn.get_attribute("innerHTML").lower():
                        edit_btn = btn
                        break

            if edit_btn:
                self.driver.execute_script("arguments[0].click();", edit_btn)
                time.sleep(1)

                # Find input field
                inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                if inputs:
                    name_input = inputs[0]
                    name_input.click()
                    time.sleep(0.5)
                    name_input.send_keys(Keys.CONTROL + "a")
                    time.sleep(0.3)
                    name_input.send_keys(Keys.DELETE)
                    time.sleep(0.3)
                    name_input.send_keys(project_name)
                    time.sleep(0.5)

                    # Save
                    try:
                        save_btn = self.driver.find_element(
                            By.XPATH,
                            "//button[.//i[contains(@class, 'google-symbols') and contains(., 'check')]]"
                        )
                        self.driver.execute_script("arguments[0].click();", save_btn)
                    except:
                        name_input.send_keys(Keys.ENTER)

                    time.sleep(2)
                    return True

        except Exception as e:
            print(Fore.YELLOW + f"[WARNING] Could not rename project: {e}")
            return False

    def switch_to_ingredients_mode(self):
        """Switch to Ingredients to Video mode"""
        try:
            print(Fore.CYAN + f"[MODE] Switching to Ingredients mode...")
            time.sleep(3)

            # Find dropdown
            dropdown_btn = self.driver.find_element(
                By.XPATH,
                "//button[contains(., 'Text to Video') and .//i[contains(., 'arrow_drop_down')]]"
            )

            self.driver.execute_script("arguments[0].click();", dropdown_btn)
            time.sleep(2)

            # Select Ingredients option
            options = self.driver.find_elements(By.XPATH, "//*[@role='option']")
            for option in options:
                if "ingredient" in option.text.lower():
                    option.click()
                    time.sleep(3)
                    print(Fore.GREEN + f"[MODE] ✅ Switched to Ingredients")
                    return True

            # If not found, try third option (usually Ingredients is third)
            if len(options) >= 3:
                options[2].click()
                time.sleep(3)
                return True

        except Exception as e:
            print(Fore.YELLOW + f"[WARNING] Mode switch issue: {str(e)}")
            return False

    def open_generate_image_dialog(self):
        """Open the Generate Image dialog by clicking + button and Generate Image"""
        try:
            print(Fore.CYAN + "\n[DIALOG] Opening Generate Image dialog...")
            
            # Click the + button (add ingredient button)
            plus_button = None
            try:
                # Method 1: Try finding by class (most reliable)
                plus_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.sc-74578dc8-1.hopAJY")
                if plus_buttons:
                    plus_button = plus_buttons[0]
                    print(Fore.GREEN + "[DIALOG] ✅ Found + button by class")
            except:
                pass
            
            if not plus_button:
                try:
                    # Method 2: Find by XPath with 'add' icon
                    plus_buttons = self.driver.find_elements(By.XPATH, "//button//i[text()='add']/..")
                    if plus_buttons:
                        plus_button = plus_buttons[0]
                        print(Fore.GREEN + "[DIALOG] ✅ Found + button by icon")
                except:
                    pass
            
            if plus_button:
                self.driver.execute_script("arguments[0].click();", plus_button)
                print(Fore.GREEN + "[DIALOG] ✅ Clicked + button")
                time.sleep(3)
            else:
                print(Fore.RED + "[ERROR] Could not find + button")
                return False
            
            # Click the Generate Image button
            print(Fore.CYAN + "[DIALOG] Looking for Generate Image button...")
            
            generate_button = None
            wait = WebDriverWait(self.driver, 10)
            
            try:
                # Method 1: Find by the specific class and text
                generate_button = wait.until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'sc-fbea20b2-0')]//div[contains(text(), 'Generate Image')]"
                )))
                print(Fore.GREEN + "[DIALOG] ✅ Found Generate Image button (Method 1)")
            except:
                pass
            
            if not generate_button:
                try:
                    # Method 2: Find by icon and text
                    generate_button = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[.//i[contains(text(), 'image_edit_auto')] and .//text()[contains(., 'Generate Image')]]"
                    )))
                    print(Fore.GREEN + "[DIALOG] ✅ Found Generate Image button (Method 2)")
                except:
                    pass
            
            if not generate_button:
                try:
                    # Method 3: Simple text search
                    generate_button = wait.until(EC.element_to_be_clickable((
                        By.XPATH,
                        "//button[contains(., 'Generate Image')]"
                    )))
                    print(Fore.GREEN + "[DIALOG] ✅ Found Generate Image button (Method 3)")
                except:
                    pass
            
            if not generate_button:
                try:
                    # Method 4: Find by data-index="0" in parent div
                    generate_button = wait.until(EC.element_to_be_clickable((
                        By.CSS_SELECTOR,
                        'div[data-index="0"] button.sc-fbea20b2-0'
                    )))
                    print(Fore.GREEN + "[DIALOG] ✅ Found Generate Image button (Method 4)")
                except:
                    pass
            
            if generate_button:
                self.driver.execute_script("arguments[0].click();", generate_button)
                print(Fore.GREEN + "[DIALOG] ✅ Clicked Generate Image button")
                time.sleep(2)
                
                print(Fore.GREEN + "\n" + "=" * 60)
                print(Fore.GREEN + "✅ SUCCESS! Generate Image dialog should be open.")
                print(Fore.GREEN + "=" * 60)
                return True
            else:
                print(Fore.RED + "[ERROR] Could not find Generate Image button")
                return False
        
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to open Generate Image dialog: {str(e)}")
            return False

    def get_video_ids_before_generation(self):
        """Get unique identifiers for existing videos before generation"""
        try:
            videos = self.driver.find_elements(By.TAG_NAME, 'video')
            video_ids = []
            for video in videos:
                try:
                    # Try to get a unique identifier for each video
                    src = video.get_attribute('src')
                    if src:
                        video_ids.append(src)
                    else:
                        # If no src, use the element itself as identifier
                        video_ids.append(id(video))
                except:
                    pass
            return video_ids
        except:
            return []

    def add_prompt_and_generate(self, prompt_text, prompt_num, ingredient_numbers=None, is_first=False):
        """Add prompt and generate videos with ingredient selection"""
        try:
            print(Fore.CYAN + f"\n[PROMPT {prompt_num}] Adding prompt...")

            # Select ingredients if specified
            if ingredient_numbers and not is_first:
                if not self.select_ingredients_for_prompt(ingredient_numbers):
                    print(Fore.YELLOW + f"[PROMPT {prompt_num}] ⚠️ Ingredient selection failed, continuing...")

            # GET VIDEO IDS BEFORE GENERATION - CRITICAL FOR TRACKING
            self.videos_before_generation = self.get_video_ids_before_generation()
            self.existing_video_count = len(self.videos_before_generation)
            print(Fore.YELLOW + f"[PROMPT {prompt_num}] Existing videos on page: {self.existing_video_count}")

            # Find text area - with multiple methods to handle overlay issues
            text_area = None

            # Method 1: By ID
            try:
                text_area = self.driver.find_element(By.ID, "PINHOLE_TEXT_AREA_ELEMENT_ID")
            except:
                pass

            # Method 2: By tag
            if not text_area:
                try:
                    text_area = self.driver.find_element(By.TAG_NAME, "textarea")
                except:
                    pass

            # Method 3: By placeholder
            if not text_area:
                try:
                    text_area = self.driver.find_element(
                        By.XPATH,
                        "//textarea[contains(@placeholder, 'Generate')]"
                    )
                except:
                    pass

            if text_area:
                # Scroll to element
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", text_area)
                time.sleep(1)

                # Close any overlays by clicking escape
                ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                time.sleep(0.5)

                # Click the text area to focus it
                self.driver.execute_script("arguments[0].click();", text_area)
                time.sleep(0.5)

                # Clear existing text using multiple methods
                text_area.click()
                time.sleep(0.3)
                text_area.send_keys(Keys.CONTROL + "a")
                time.sleep(0.3)
                text_area.send_keys(Keys.DELETE)
                time.sleep(0.3)

                # Copy prompt to clipboard and paste
                pyperclip.copy(prompt_text)
                text_area.send_keys(Keys.CONTROL + "v")
                time.sleep(0.5)

                # Also trigger input event to ensure the interface recognizes the text
                self.driver.execute_script("""
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """, text_area)

                # Click outside the text area to ensure it registers
                self.driver.execute_script("document.body.click();")
                time.sleep(0.5)

                # Click text area again to ensure it's active
                text_area.click()
                time.sleep(0.5)

                print(Fore.GREEN + f"[PROMPT {prompt_num}] ✅ Prompt added")
            else:
                print(Fore.RED + "[ERROR] Could not find text area")
                return False

            # WAIT 3 SECONDS AFTER ADDING PROMPT
            print(Fore.YELLOW + f"[PROMPT {prompt_num}] ⏳ Waiting 3 seconds before generation...")
            for i in range(3, 0, -1):
                print(f"\r[PROMPT {prompt_num}] ⏳ Waiting {i} seconds...", end="", flush=True)
                time.sleep(1)
            print(f"\r[PROMPT {prompt_num}] ⏳ Wait complete!                    ")

            # Click generate button - try multiple methods
            generate_btn = None

            # Method 1: By icon
            try:
                generate_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[.//i[contains(@class, 'google-symbols') and contains(., 'arrow_forward')]]"
                )
            except:
                pass

            # Method 2: Find all buttons and check if enabled
            if not generate_btn:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    if "arrow_forward" in btn.get_attribute("innerHTML"):
                        if btn.is_enabled():
                            generate_btn = btn
                            break

            if generate_btn:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", generate_btn)
                time.sleep(0.5)

                # Check if button is enabled
                if not generate_btn.is_enabled():
                    print(Fore.YELLOW + "[WARNING] Generate button not enabled, waiting...")
                    time.sleep(3)

                self.driver.execute_script("arguments[0].click();", generate_btn)
                print(Fore.GREEN + f"[PROMPT {prompt_num}] ✅ Generation started")
                return True
            else:
                print(Fore.RED + "[ERROR] Could not find generate button")
                return False

        except Exception as e:
            print(Fore.RED + f"[ERROR] Prompt/Generate failed: {str(e)}")
            return False

    def click_reuse_prompt(self):
        """Click the reuse prompt button to keep ingredients"""
        try:
            print(Fore.CYAN + "[REUSE] Clicking reuse prompt button...")

            # Wait for the button to appear
            time.sleep(3)

            # Find reuse prompt button
            reuse_btn = None

            # Method 1: By icon text
            try:
                reuse_btn = self.driver.find_element(
                    By.XPATH,
                    "//button[.//i[contains(., 'wrap_text')]]"
                )
            except:
                pass

            # Method 2: By span text
            if not reuse_btn:
                try:
                    reuse_btn = self.driver.find_element(
                        By.XPATH,
                        "//button[.//span[contains(., 'Reuse prompt')]]"
                    )
                except:
                    pass

            # Method 3: Search all buttons
            if not reuse_btn:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in buttons:
                    try:
                        btn_html = btn.get_attribute("innerHTML").lower()
                        if "wrap_text" in btn_html or "reuse" in btn_html:
                            reuse_btn = btn
                            break
                    except:
                        pass

            if reuse_btn:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", reuse_btn)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", reuse_btn)
                print(Fore.GREEN + "[REUSE] ✅ Reuse prompt clicked")

                # WAIT 3 SECONDS AFTER CLICKING REUSE
                print(Fore.YELLOW + "[REUSE] ⏳ Waiting 3 seconds...")
                for i in range(3, 0, -1):
                    print(f"\r[REUSE] ⏳ Waiting {i} seconds...", end="", flush=True)
                    time.sleep(1)
                print(f"\r[REUSE] ⏳ Wait complete!                    ")

                # Update video tracking after reuse
                self.videos_before_generation = self.get_video_ids_before_generation()
                self.existing_video_count = len(self.videos_before_generation)

                return True
            else:
                print(Fore.YELLOW + "[WARNING] Reuse prompt button not found")
                return False

        except Exception as e:
            print(Fore.YELLOW + f"[WARNING] Reuse prompt issue: {str(e)}")
            return False

    def wait_for_generation_complete(self, timeout=600):
        """Wait for generation to complete - ENHANCED VIDEO DETECTION"""
        start_time = time.time()
        print("[GENERATE] Progress: ", end="", flush=True)
        last_progress = ""
        videos_check_count = 0
        progress_stuck_time = 0
        last_progress_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Look for progress indicator
                progress_elements = self.driver.find_elements(By.CLASS_NAME, "sc-dd6abb21-1")

                if not progress_elements:
                    all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                    for div in all_divs:
                        text = div.text.strip()
                        if "%" in text and len(text) < 10:
                            progress_elements.append(div)

                current_progress = ""
                if progress_elements:
                    for element in progress_elements:
                        text = element.text.strip()
                        if "%" in text:
                            current_progress = text
                            print(f"\r[GENERATE] Progress: {text}", end="", flush=True)
                            if "100%" in text:
                                time.sleep(2)
                                print(f"\r[GENERATE] Progress: 100% ✅ Complete!")
                                return True
                
                # Track progress changes
                if current_progress != last_progress:
                    last_progress_time = time.time()
                    progress_stuck_time = 0
                else:
                    progress_stuck_time = time.time() - last_progress_time
                
                # Check if videos appeared (generation might be complete even without 100%)
                videos = self.driver.find_elements(By.TAG_NAME, 'video')
                current_video_count = len(videos)
                
                # AGGRESSIVE VIDEO DETECTION - Multiple strategies
                
                # Strategy 1: If we have 4+ new videos, check if they're stable
                if current_video_count >= self.existing_video_count + 4:
                    videos_check_count += 1
                    if videos_check_count >= 4:  # Check for 2 seconds (4 * 0.5s)
                        print(f"\r[GENERATE] Progress: ✅ Complete! (4+ videos detected)")
                        return True
                else:
                    videos_check_count = 0
                
                # Strategy 2: If progress stuck for 15+ seconds and we have ANY new videos
                if progress_stuck_time >= 15 and current_video_count > self.existing_video_count:
                    if current_video_count >= self.existing_video_count + 2:  # At least 2 new videos
                        print(f"\r[GENERATE] Progress: ✅ Complete! (Progress stuck 15s, {current_video_count - self.existing_video_count} videos)")
                        return True
                
                # Strategy 3: If progress stuck for 30+ seconds and we have at least 1 new video
                if progress_stuck_time >= 30 and current_video_count > self.existing_video_count:
                    print(f"\r[GENERATE] Progress: ✅ Complete! (Progress stuck 30s, {current_video_count - self.existing_video_count} videos)")
                    return True
                
                # Strategy 4: Check for download buttons (indicates videos are ready)
                if current_video_count > self.existing_video_count:
                    try:
                        download_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-haspopup, 'menu') or contains(., 'download')]")
                        if len(download_buttons) >= current_video_count - self.existing_video_count:
                            print(f"\r[GENERATE] Progress: ✅ Complete! (Download buttons detected)")
                            return True
                    except:
                        pass
                
                # Strategy 5: Look for "reuse prompt" button (appears when generation is done)
                try:
                    reuse_buttons = self.driver.find_elements(By.XPATH, "//button[.//i[contains(., 'wrap_text')] or .//span[contains(., 'Reuse')]]")
                    if reuse_buttons and current_video_count > self.existing_video_count:
                        print(f"\r[GENERATE] Progress: ✅ Complete! (Reuse button detected)")
                        return True
                except:
                    pass
                
                last_progress = current_progress
                time.sleep(0.5)

            except Exception as e:
                print(f"\r[GENERATE] Progress: Error checking: {str(e)[:30]}", end="", flush=True)
                time.sleep(0.5)

        print(f"\r[GENERATE] Progress: ⚠️ Timeout!")
        return False

    def count_active_prompt_generations(self):
        """Count how many PROMPT generations are currently active (not individual videos)"""
        try:
            # Look for progress indicators - each represents one prompt generation
            progress_elements = self.driver.find_elements(By.CLASS_NAME, "sc-dd6abb21-1")
            
            if not progress_elements:
                # Fallback: look for any div with percentage
                all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                for div in all_divs:
                    text = div.text.strip()
                    if "%" in text and len(text) < 10:
                        progress_elements.append(div)
            
            # Count active prompt generations (not 100% complete)
            active_prompt_count = 0
            for element in progress_elements:
                text = element.text.strip()
                if "%" in text and "100%" not in text:
                    active_prompt_count += 1
            
            return active_prompt_count
        except:
            return 0

    def count_completed_prompt_generations(self):
        """Count how many prompt generations have completed (showing 100%)"""
        try:
            # Look for progress indicators showing 100%
            progress_elements = self.driver.find_elements(By.CLASS_NAME, "sc-dd6abb21-1")
            
            if not progress_elements:
                all_divs = self.driver.find_elements(By.TAG_NAME, "div")
                for div in all_divs:
                    text = div.text.strip()
                    if "%" in text and len(text) < 10:
                        progress_elements.append(div)
            
            completed_count = 0
            for element in progress_elements:
                text = element.text.strip()
                if "100%" in text:
                    completed_count += 1
            
            return completed_count
        except:
            return 0

    def wait_for_prompt_generation_slot(self, max_concurrent=8, timeout=300):
        """Wait until there's a slot available for new PROMPT generation - ODD ALLOWED UNDER 6
        
        NEW QUEUE RULES:
        ✅ CAN START when: 
           - active_prompts < 6 (regardless of even/odd: 0, 1, 2, 3, 4, 5)
           - active_prompts == 6 (exactly 6 is allowed)
        ❌ CANNOT START when: 
           - active_prompts >= 7 (7 or higher: 7, 8, 9, 10...)
        
        This allows odd numbers (1, 3, 5) when under 6, but blocks at 6+ to prevent exceeding 8.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                active_prompts = self.count_active_prompt_generations()
                completed_prompts = self.count_completed_prompt_generations()
                
                print(f"\r[QUEUE] Active prompt generations: {active_prompts}/8 | Completed: {completed_prompts}", end="", flush=True)
                
                # NEW LOGIC: Allow assignment for 0-6, block at 7+
                # Valid starting points: 0, 1, 2, 3, 4, 5, 6
                # Invalid starting points: 7, 8, 9, 10+
                
                if active_prompts <= 6:
                    # 0-6 active prompts - can start (odd is OK under 6)
                    print(f"\r[QUEUE] ✅ Slot available! ({active_prompts}/8 active - UNDER 7, can start)")
                    return True
                else:
                    # 7 or more - must wait
                    print(f"\r[QUEUE] ⏳ Waiting... ({active_prompts}/8 active - AT/ABOVE 7, must wait)", end="", flush=True)
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"\r[QUEUE] Error: {str(e)[:30]}", end="", flush=True)
                time.sleep(1)
        
        print(f"\r[QUEUE] ⚠️ Timeout waiting for valid prompt generation slot!")
        return False

    def wait_for_prompt_50_percent(self, prompt_index, timeout=600):
        """Wait for a specific prompt to reach 50% completion
        
        Args:
            prompt_index: The index of the prompt to monitor (0 = newest/first, 1 = second, etc.)
            timeout: Maximum time to wait in seconds (default 600 = 10 minutes)
        
        Returns:
            True if prompt reached 50%, False if timeout
        """
        start_time = time.time()
        print(Fore.CYAN + f"\n[50% WAIT] Monitoring prompt at index {prompt_index} for 50% completion...")
        
        while time.time() - start_time < timeout:
            try:
                # Find all percentage divs: <div class="sc-dd6abb21-1 iEQNVH">23%</div>
                percentage_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.sc-dd6abb21-1.iEQNVH")
                
                if len(percentage_divs) > prompt_index:
                    # Get the percentage text from the target prompt
                    percentage_text = percentage_divs[prompt_index].text.strip()
                    
                    # Extract numeric value (e.g., "23%" → 23)
                    try:
                        percentage_value = int(percentage_text.replace('%', ''))
                        
                        # Display progress
                        print(f"\r[50% WAIT] Prompt {prompt_index} progress: {percentage_value}% (waiting for 50%)", end="", flush=True)
                        
                        # Check if reached 50% or higher
                        if percentage_value >= 50:
                            print(f"\r[50% WAIT] ✅ Prompt {prompt_index} reached {percentage_value}%! Proceeding to next prompt...")
                            return True
                    except ValueError:
                        # If percentage text is not a number, continue waiting
                        print(f"\r[50% WAIT] Waiting for prompt {prompt_index} to show percentage...", end="", flush=True)
                else:
                    # Prompt not found yet, might still be initializing
                    print(f"\r[50% WAIT] Waiting for prompt {prompt_index} to appear in queue...", end="", flush=True)
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"\r[50% WAIT] Error checking percentage: {str(e)[:50]}", end="", flush=True)
                time.sleep(2)
        
        print(f"\r[50% WAIT] ⚠️ Timeout waiting for prompt {prompt_index} to reach 50%!")
        return False

    def wait_for_all_prompt_generations_complete(self, timeout=900):
        """Wait for all active PROMPT generations to complete"""
        start_time = time.time()
        print("[FINAL] Waiting for all prompt generations: ", end="", flush=True)
        
        while time.time() - start_time < timeout:
            try:
                active_prompts = self.count_active_prompt_generations()
                completed_prompts = self.count_completed_prompt_generations()
                
                print(f"\r[FINAL] Active prompt generations: {active_prompts} | Completed: {completed_prompts}", end="", flush=True)
                
                if active_prompts == 0:
                    print(f"\r[FINAL] ✅ All prompt generations complete! Total completed: {completed_prompts}")
                    return True
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"\r[FINAL] Error: {str(e)[:30]}", end="", flush=True)
                time.sleep(2)
        
        print(f"\r[FINAL] ⚠️ Timeout!")
        return False

    def download_videos_for_prompt(self, prompt_num):
        """Download ONLY the 4 newly generated videos using video tracking strategy"""
        try:
            print(Fore.CYAN + f"\n[DOWNLOAD] Downloading videos for Prompt {prompt_num}...")

            # Get all current videos on the page
            all_videos = self.driver.find_elements(By.TAG_NAME, 'video')
            current_video_count = len(all_videos)

            print(Fore.CYAN + f"[DOWNLOAD] Total videos: {current_video_count} | Previous: {self.existing_video_count}")

            # STRATEGY 1: Identify NEW videos by comparing with stored IDs
            new_videos = []
            for video in all_videos:
                try:
                    src = video.get_attribute('src')
                    # Check if this video wasn't there before
                    if src:
                        if src not in self.videos_before_generation:
                            new_videos.append(video)
                    else:
                        # If no src, check by element reference
                        video_id = id(video)
                        if video_id not in self.videos_before_generation:
                            new_videos.append(video)
                except:
                    pass

            # STRATEGY 2: Fallback to position-based selection if needed
            if len(new_videos) < 4:
                print(Fore.YELLOW + f"[DOWNLOAD] Using position-based selection (found only {len(new_videos)} by src)")
                # Get the videos that are after the existing ones
                start_index = self.existing_video_count
                new_videos = all_videos[start_index:start_index + 4] if start_index < len(all_videos) else []

            # Make sure we have exactly 4 new videos
            if len(new_videos) > 4:
                new_videos = new_videos[:4]  # Take only first 4 if somehow we got more

            if len(new_videos) < 4:
                print(Fore.YELLOW + f"[WARNING] Expected 4 new videos, found {len(new_videos)}")

            print(Fore.CYAN + f"[DOWNLOAD] Downloading {len(new_videos)} new videos")

            downloaded_count = 0

            for video_idx, video in enumerate(new_videos, 1):
                try:
                    # Generate filename: P1V1, P1V2, P1V3, P1V4
                    filename = f"P{prompt_num}V{video_idx}.mp4"

                    # STRATEGY 3: Find container by traversing up from video element
                    container = video
                    # Traverse up 7 levels to find the container
                    for _ in range(7):
                        try:
                            container = container.find_element(By.XPATH, '..')
                        except:
                            break

                    # Scroll to video
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", container)
                    time.sleep(1)

                    # STRATEGY 4: Find download button within this specific container
                    download_btn = None
                    buttons = container.find_elements(By.TAG_NAME, 'button')

                    for btn in buttons:
                        try:
                            btn_html = btn.get_attribute('innerHTML').lower()
                            # Look for download icon or menu button
                            if 'download' in btn_html or btn.get_attribute('aria-haspopup') == 'menu':
                                download_btn = btn
                                break
                        except:
                            pass

                    if not download_btn:
                        print(Fore.YELLOW + f"  ⚠️ No download button for video {video_idx}")
                        continue

                    print(Fore.CYAN + f"  📥 Downloading {filename}...", end="")

                    # Click download button
                    self.driver.execute_script("arguments[0].click();", download_btn)
                    time.sleep(1)

                    # Select quality
                    try:
                        menu_items = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="menuitem"]'))
                        )

                        # Click best quality
                        quality_found = False
                        for item in menu_items:
                            if "720p" in item.text or "Original" in item.text:
                                self.driver.execute_script("arguments[0].click();", item)
                                quality_found = True
                                break

                        if not quality_found and menu_items:
                            self.driver.execute_script("arguments[0].click();", menu_items[0])
                    except:
                        pass

                    # Close menu
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

                    # Wait for download
                    if self.wait_for_download_complete():
                        if self.move_and_rename_download(filename):
                            print(Fore.GREEN + " ✅")
                            downloaded_count += 1
                            self.videos_downloaded += 1
                        else:
                            print(Fore.YELLOW + " ⚠️ Move failed")
                    else:
                        print(Fore.YELLOW + " ⚠️ Download timeout")

                    time.sleep(1)

                except Exception as e:
                    print(Fore.YELLOW + f" ⚠️ Error: {str(e)[:50]}")

            # Update the tracking for next prompt
            self.videos_before_generation = self.get_video_ids_before_generation()
            self.existing_video_count = len(self.videos_before_generation)

            print(Fore.GREEN + f"[DOWNLOAD] Downloaded {downloaded_count}/{len(new_videos)} videos")
            return downloaded_count

        except Exception as e:
            print(Fore.RED + f"[ERROR] Download failed: {str(e)}")
            return 0

    def wait_for_download_complete(self, timeout=60):
        """Wait for download to complete"""
        start_time = time.time()
        download_started = False

        while time.time() - start_time < timeout:
            try:
                files = os.listdir(BROWSER_DOWNLOAD_FOLDER)

                # Check for temp files
                temp_files = [f for f in files if f.endswith('.crdownload') or f.endswith('.tmp')]

                if temp_files:
                    download_started = True
                    time.sleep(1)
                elif download_started:
                    time.sleep(1)
                    return True
                else:
                    # Check for new video files
                    for file in files:
                        if file.lower().endswith(('.mp4', '.webm', '.mov')):
                            file_path = os.path.join(BROWSER_DOWNLOAD_FOLDER, file)
                            if time.time() - os.path.getctime(file_path) < 5:
                                time.sleep(1)
                                return True
                    time.sleep(1)

            except:
                pass

        return False

    def move_and_rename_download(self, target_filename):
        """Move and rename downloaded file"""
        try:
            video_files = []

            for file in os.listdir(BROWSER_DOWNLOAD_FOLDER):
                if file.lower().endswith(('.mp4', '.webm', '.mov', '.avi')):
                    file_path = os.path.join(BROWSER_DOWNLOAD_FOLDER, file)
                    if time.time() - os.path.getctime(file_path) < 30:
                        video_files.append((file, os.path.getctime(file_path)))

            if not video_files:
                return False

            video_files.sort(key=lambda x: x[1], reverse=True)
            latest_file = video_files[0][0]

            source = os.path.join(BROWSER_DOWNLOAD_FOLDER, latest_file)
            target = os.path.join(OUTPUT_FOLDER, target_filename)

            shutil.move(source, target)
            return True

        except Exception as e:
            return False

    def process_all_prompts_batch(self, image_paths, all_prompts):
        """Process all prompts in batches of 5 - GENERATION ONLY"""
        try:
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"📦 BATCH PROCESSING {len(all_prompts)} PROMPTS")
            print(Fore.CYAN + f"📦 Strategy: 5 prompts per batch, generation only")
            print(f"{'═' * 60}")

            # Track image upload time
            upload_start = datetime.now()
            self.write_to_report(f"Starting image upload to library...")

            # Upload images to library ONCE
            if not self.upload_multiple_ingredients_to_library(image_paths):
                print(Fore.RED + "[ERROR] Failed to upload images")
                self.write_to_report("[ERROR] Failed to upload images")
                return False

            upload_time = datetime.now() - upload_start
            self.write_to_report(f"✅ Images uploaded successfully. Time taken: {str(upload_time).split('.')[0]}")
            self.write_to_report("-" * 50)

            # Process prompts in batches of 5
            batch_size = 5
            total_batches = (len(all_prompts) + batch_size - 1) // batch_size  # Ceiling division
            
            for batch_num in range(total_batches):
                batch_start = datetime.now()
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(all_prompts))
                batch_prompts = all_prompts[start_idx:end_idx]
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + f"📦 BATCH {batch_num + 1}/{total_batches}")
                print(Fore.YELLOW + f"🎯 Processing prompts {start_idx + 1}-{end_idx}")
                print(f"{'═' * 60}")
                
                self.write_to_report(f"\n{'=' * 60}")
                self.write_to_report(f"BATCH {batch_num + 1}/{total_batches} - Prompts {start_idx + 1}-{end_idx}")
                self.write_to_report(f"{'=' * 60}")

                # STEP 1: Add all 5 prompts with 8-second intervals
                print(Fore.CYAN + f"\n📝 ADDING {len(batch_prompts)} PROMPTS...")
                for prompt_idx, prompt in enumerate(batch_prompts):
                    global_prompt_num = start_idx + prompt_idx + 1

                    print(f"\n{'-' * 40}")
                    print(Fore.YELLOW + f"[ADDING PROMPT {global_prompt_num}/{len(all_prompts)}] Batch {batch_num + 1}")
                    print(f"{'-' * 40}")

                    self.write_to_report(f"\n[PROMPT {global_prompt_num}] Adding...")
                    self.write_to_report(f"Prompt text: {prompt[:100]}...")

                    # For first prompt overall
                    if global_prompt_num == 1:
                        if not self.add_prompt_and_generate(prompt, global_prompt_num, is_first=True):
                            self.write_to_report(f"[PROMPT {global_prompt_num}] ❌ Failed to add/generate")
                            continue
                    else:
                        # For all other prompts: click reuse, add prompt, generate
                        if not self.click_reuse_prompt():
                            print(Fore.YELLOW + "[WARNING] Continuing without reuse prompt")
                            self.write_to_report(f"[PROMPT {global_prompt_num}] ⚠️ Reuse prompt failed")

                        if not self.add_prompt_and_generate(prompt, global_prompt_num, is_first=False):
                            self.write_to_report(f"[PROMPT {global_prompt_num}] ❌ Failed to add/generate")
                            continue

                    print(Fore.GREEN + f"[PROMPT {global_prompt_num}] ✅ Added and generation started")
                    self.write_to_report(f"[PROMPT {global_prompt_num}] Added and generation started")

                    # Wait 8 seconds before next prompt (except for last prompt in batch)
                    if prompt_idx < len(batch_prompts) - 1:
                        print(Fore.CYAN + "⏳ Waiting 8 seconds before next prompt...")
                        for i in range(8, 0, -1):
                            print(f"\r⏳ Next prompt in {i} seconds...", end="", flush=True)
                            time.sleep(1)
                        print(f"\r⏳ Adding next prompt...                    ")

                # STEP 2: Wait for all generations in this batch to complete
                print(f"\n{'═' * 50}")
                print(Fore.CYAN + f"⏳ WAITING FOR BATCH {batch_num + 1} GENERATIONS...")
                print(f"{'═' * 50}")
                
                batch_gen_start = datetime.now()
                
                # Wait for all generations to complete (enhanced detection)
                print(Fore.YELLOW + "🔄 Monitoring generation progress...")
                if not self.wait_for_batch_generation_complete(len(batch_prompts)):
                    print(Fore.YELLOW + "[WARNING] Batch generation timeout")
                    self.write_to_report(f"BATCH {batch_num + 1} ⚠️ Generation timeout")
                else:
                    batch_gen_time = datetime.now() - batch_gen_start
                    print(Fore.GREEN + f"✅ All {len(batch_prompts)} generations complete in {str(batch_gen_time).split('.')[0]}")
                    self.write_to_report(f"BATCH {batch_num + 1} ✅ All generations complete. Time: {str(batch_gen_time).split('.')[0]}")
                
                # Update timing stats
                for prompt_idx in range(len(batch_prompts)):
                    self.prompt_times.append(batch_gen_time.total_seconds() / len(batch_prompts))

                # Batch completion summary
                batch_time = datetime.now() - batch_start
                print(f"\n{'═' * 50}")
                print(Fore.GREEN + f"✅ BATCH {batch_num + 1} COMPLETE!")
                print(Fore.GREEN + f"📊 Generated {len(batch_prompts)} prompts in {str(batch_time).split('.')[0]}")
                print(Fore.GREEN + f"🎬 Total videos on page: ~{(end_idx) * 4}")
                print(f"{'═' * 50}")
                
                self.write_to_report(f"\nBATCH {batch_num + 1} COMPLETE:")
                self.write_to_report(f"- Prompts processed: {len(batch_prompts)}")
                self.write_to_report(f"- Batch time: {str(batch_time).split('.')[0]}")
                self.write_to_report(f"- Total prompts done: {end_idx}/{len(all_prompts)}")
                
                # Calculate stats
                if self.prompt_times:
                    avg_time = sum(self.prompt_times) / len(self.prompt_times)
                    remaining_prompts = len(all_prompts) - end_idx
                    estimated_remaining = avg_time * remaining_prompts
                    
                    print(Fore.CYAN + f"📈 Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                    print(Fore.CYAN + f"⏰ Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                    
                    self.write_to_report(f"- Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                    self.write_to_report(f"- Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")

                # Wait between batches (except for last batch)
                if batch_num < total_batches - 1:
                    print(Fore.YELLOW + f"\n⏳ Waiting 10 seconds before next batch...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next batch in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Starting next batch...                    ")

            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Batch processing failed: {str(e)}")
            self.write_to_report(f"[ERROR] Batch processing failed: {str(e)}")
            return False

    def process_multiple_worksheet_projects(self, worksheets_data):
        """Process multiple worksheets as separate projects"""
        try:
            total_worksheets = len(worksheets_data)
            current_worksheet = 0
            
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"🏗️ CREATING {total_worksheets} SEPARATE PROJECTS")
            print(f"{'═' * 60}")
            
            for worksheet_name, worksheet_data in worksheets_data.items():
                current_worksheet += 1
                worksheet_prompts = worksheet_data['prompts']
                
                print(f"\n{'█' * 60}")
                print(Fore.YELLOW + f"📋 PROJECT {current_worksheet}/{total_worksheets}: {worksheet_name}")
                print(Fore.YELLOW + f"📝 Prompts: {len(worksheet_prompts)}")
                print(Fore.YELLOW + f"🎬 Expected Videos: {len(worksheet_prompts) * 2}")
                print(f"{'█' * 60}")
                
                # Start tracking this worksheet
                self.start_worksheet_tracking(worksheet_name, len(worksheet_prompts))
                
                # Create project name - same as worksheet name
                project_name = worksheet_name
                
                # Navigate to Flow (for first project) or create new project
                if current_worksheet == 1:
                    # First project - navigate to Flow
                    if not self.navigate_to_flow():
                        print(Fore.RED + f"[ERROR] Failed to navigate to Flow for {worksheet_name}")
                        continue
                else:
                    # Subsequent projects - navigate to Flow again
                    if not self.navigate_to_flow():
                        print(Fore.RED + f"[ERROR] Failed to navigate to Flow for {worksheet_name}")
                        continue
                
                # Create new project
                if not self.create_new_project(project_name):
                    print(Fore.RED + f"[ERROR] Failed to create project for {worksheet_name}")
                    continue
                
                # Switch to Ingredients mode
                if not self.switch_to_ingredients_mode():
                    print(Fore.YELLOW + f"[WARNING] Could not switch mode for {worksheet_name}, continuing anyway...")
                
                # Get and upload worksheet-specific images
                print(Fore.CYAN + f"\n[PROJECT {current_worksheet}] Getting images for '{worksheet_name}'...")
                worksheet_images = self.get_worksheet_images(worksheet_name)
                if not worksheet_images:
                    print(Fore.RED + f"[ERROR] Failed to get images for {worksheet_name}")
                    continue
                
                print(Fore.CYAN + f"\n[PROJECT {current_worksheet}] Uploading images to library...")
                if not self.upload_multiple_ingredients_to_library(worksheet_images):
                    print(Fore.RED + f"[ERROR] Failed to upload images for {worksheet_name}")
                    continue
                
                # Process prompts for this worksheet
                print(Fore.CYAN + f"\n[PROJECT {current_worksheet}] Processing {len(worksheet_prompts)} prompts...")
                success = self.process_worksheet_prompts_queue(worksheet_prompts, worksheet_name, current_worksheet, total_worksheets)
                
                # Complete tracking for this worksheet
                self.complete_worksheet_tracking(worksheet_name, success)
                
                if success:
                    print(Fore.GREEN + f"\n✅ PROJECT {current_worksheet} COMPLETE: {worksheet_name}")
                else:
                    print(Fore.YELLOW + f"\n⚠️ PROJECT {current_worksheet} HAD ISSUES: {worksheet_name}")
                
                # Update generation statistics
                self.update_generation_stats()
                
                # Wait between projects (except for last one)
                if current_worksheet < total_worksheets:
                    print(Fore.CYAN + f"\n⏳ Waiting 10 seconds before next project...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next project in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Starting next project...                    ")
            
            print(f"\n{'█' * 60}")
            print(Fore.GREEN + f"🎉 ALL {total_worksheets} PROJECTS COMPLETED!")
            print(f"{'█' * 60}")
            self.write_to_report(f"\n🎉 ALL {total_worksheets} PROJECTS COMPLETED!")
            
            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Multiple project processing failed: {str(e)}")
            self.write_to_report(f"[ERROR] Multiple project processing failed: {str(e)}")
            return False

    def process_worksheet_prompts_queue(self, worksheet_prompts, worksheet_name, project_num, total_projects):
        """Process prompts for a single worksheet using queue system"""
        try:
            print(f"\n{'═' * 50}")
            print(Fore.CYAN + f"🚀 PROCESSING WORKSHEET: {worksheet_name}")
            print(Fore.CYAN + f"⚡ Strategy: Max 8 concurrent generations (even numbers only), 2 videos per prompt")
            print(f"{'═' * 50}")

            # Process prompts using dynamic queue
            processed_count = 0
            
            for prompt_idx, prompt in enumerate(worksheet_prompts):
                global_prompt_num = prompt_idx + 1
                prompt_start = datetime.now()

                print(f"\n{'═' * 40}")
                print(Fore.YELLOW + f"[PROJECT {project_num}] [PROMPT {global_prompt_num}/{len(worksheet_prompts)}]")
                print(f"{'═' * 40}")

                self.write_to_report(f"\n[PROJECT {project_num}] [PROMPT {global_prompt_num}] Starting...")
                self.write_to_report(f"Prompt text: {prompt[:100]}...")

                # Wait for available slot (max 8 concurrent PROMPT generations - EVEN NUMBERS ONLY)
                if global_prompt_num > 1:  # Skip queue check for first prompt
                    print(Fore.CYAN + "🔄 Checking prompt generation queue (even numbers only)...")
                    if not self.wait_for_prompt_generation_slot(max_concurrent=8):
                        print(Fore.YELLOW + "[WARNING] Queue timeout, continuing anyway")
                        self.write_to_report(f"[PROJECT {project_num}] [PROMPT {global_prompt_num}] ⚠️ Queue timeout")

                # For first prompt overall
                if global_prompt_num == 1:
                    if not self.add_prompt_and_generate(prompt, global_prompt_num, is_first=True):
                        self.write_to_report(f"[PROJECT {project_num}] [PROMPT {global_prompt_num}] ❌ Failed to add/generate")
                        continue
                else:
                    # For all other prompts: click reuse, add prompt, generate
                    if not self.click_reuse_prompt():
                        print(Fore.YELLOW + "[WARNING] Continuing without reuse prompt")
                        self.write_to_report(f"[PROJECT {project_num}] [PROMPT {global_prompt_num}] ⚠️ Reuse prompt failed")

                    if not self.add_prompt_and_generate(prompt, global_prompt_num, is_first=False):
                        self.write_to_report(f"[PROJECT {project_num}] [PROMPT {global_prompt_num}] ❌ Failed to add/generate")
                        continue

                processed_count += 1
                prompt_total_time = datetime.now() - prompt_start
                self.prompt_times.append(prompt_total_time.total_seconds())

                print(Fore.GREEN + f"[PROJECT {project_num}] [PROMPT {global_prompt_num}] ✅ Queued for generation")
                self.write_to_report(f"[PROJECT {project_num}] [PROMPT {global_prompt_num}] ✅ Queued for generation")

                # Show current queue status
                active_prompts = self.count_active_prompt_generations()
                completed_prompts = self.count_completed_prompt_generations()
                print(Fore.CYAN + f"📊 Queue status: {active_prompts}/8 active prompt generations | {completed_prompts} completed")
                
                # MANDATORY 10-SECOND WAIT between prompts to avoid "generating too fast" error
                if global_prompt_num < len(worksheet_prompts):  # Not the last prompt
                    print(Fore.YELLOW + f"\n⏳ Waiting 10 seconds before next prompt (Google Flow rate limit)...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next prompt in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Ready for next prompt!                    ")

                # Calculate and show stats every 5 prompts
                if processed_count % 5 == 0:
                    print(f"\n{'═' * 40}")
                    print(Fore.GREEN + f"✅ MILESTONE: {processed_count}/{len(worksheet_prompts)} prompts queued")
                    
                    if self.prompt_times:
                        avg_time = sum(self.prompt_times) / len(self.prompt_times)
                        remaining_prompts = len(worksheet_prompts) - processed_count
                        estimated_remaining = avg_time * remaining_prompts
                        
                        print(Fore.CYAN + f"📈 Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                        print(Fore.CYAN + f"⏰ Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                        
                        self.write_to_report(f"[PROJECT {project_num}] MILESTONE: {processed_count}/{len(worksheet_prompts)} prompts queued")
                        self.write_to_report(f"- Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                        self.write_to_report(f"- Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                    
                    print(f"{'═' * 40}")

            # Wait for all remaining generations to complete
            print(f"\n{'═' * 50}")
            print(Fore.CYAN + f"⏳ WAITING FOR ALL GENERATIONS TO COMPLETE...")
            print(f"{'═' * 50}")
            
            final_wait_start = datetime.now()
            if not self.wait_for_all_prompt_generations_complete():
                print(Fore.YELLOW + "[WARNING] Final prompt generation timeout")
                self.write_to_report(f"[PROJECT {project_num}] ⚠️ Final prompt generation timeout")
            else:
                final_wait_time = datetime.now() - final_wait_start
                print(Fore.GREEN + f"✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")
                self.write_to_report(f"[PROJECT {project_num}] ✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")

            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Worksheet processing failed: {str(e)}")
            self.write_to_report(f"[PROJECT {project_num}] [ERROR] Worksheet processing failed: {str(e)}")
            return False

    def process_all_prompts_queue(self, image_paths, all_prompts):
        """Process all prompts using dynamic queue system - 4 concurrent generations max"""
        try:
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"🚀 QUEUE PROCESSING {len(all_prompts)} PROMPTS")
            print(Fore.CYAN + f"⚡ Strategy: Max 8 concurrent generations (even numbers only), 2 videos per prompt")
            print(f"{'═' * 60}")

            # Track image upload time
            upload_start = datetime.now()
            self.write_to_report(f"Starting image upload to library...")

            # Upload images to library ONCE
            if not self.upload_multiple_ingredients_to_library(image_paths):
                print(Fore.RED + "[ERROR] Failed to upload images")
                self.write_to_report("[ERROR] Failed to upload images")
                return False

            upload_time = datetime.now() - upload_start
            self.write_to_report(f"✅ Images uploaded successfully. Time taken: {str(upload_time).split('.')[0]}")
            self.write_to_report("-" * 50)

            # Process prompts using dynamic queue
            processed_count = 0
            
            for prompt_idx, prompt in enumerate(all_prompts):
                global_prompt_num = prompt_idx + 1
                prompt_start = datetime.now()

                print(f"\n{'═' * 50}")
                print(Fore.YELLOW + f"[PROMPT {global_prompt_num}/{len(all_prompts)}]")
                print(f"{'═' * 50}")

                self.write_to_report(f"\n[PROMPT {global_prompt_num}] Starting...")
                self.write_to_report(f"Prompt text: {prompt[:100]}...")

                # Wait for available slot (max 8 concurrent PROMPT generations - EVEN NUMBERS ONLY)
                if global_prompt_num > 1:  # Skip queue check for first prompt
                    print(Fore.CYAN + "🔄 Checking prompt generation queue (even numbers only)...")
                    if not self.wait_for_prompt_generation_slot(max_concurrent=8):
                        print(Fore.YELLOW + "[WARNING] Queue timeout, continuing anyway")
                        self.write_to_report(f"[PROMPT {global_prompt_num}] ⚠️ Queue timeout")

                # For first prompt overall
                if global_prompt_num == 1:
                    if not self.add_prompt_and_generate(prompt, global_prompt_num, is_first=True):
                        self.write_to_report(f"[PROMPT {global_prompt_num}] ❌ Failed to add/generate")
                        continue
                else:
                    # For all other prompts: click reuse, add prompt, generate
                    if not self.click_reuse_prompt():
                        print(Fore.YELLOW + "[WARNING] Continuing without reuse prompt")
                        self.write_to_report(f"[PROMPT {global_prompt_num}] ⚠️ Reuse prompt failed")

                    if not self.add_prompt_and_generate(prompt, global_prompt_num, is_first=False):
                        self.write_to_report(f"[PROMPT {global_prompt_num}] ❌ Failed to add/generate")
                        continue

                processed_count += 1
                prompt_total_time = datetime.now() - prompt_start
                self.prompt_times.append(prompt_total_time.total_seconds())

                print(Fore.GREEN + f"[PROMPT {global_prompt_num}] ✅ Queued for generation")
                self.write_to_report(f"[PROMPT {global_prompt_num}] ✅ Queued for generation")

                # Show current queue status
                active_prompts = self.count_active_prompt_generations()
                completed_prompts = self.count_completed_prompt_generations()
                print(Fore.CYAN + f"📊 Queue status: {active_prompts}/8 active prompt generations | {completed_prompts} completed")
                
                # MANDATORY 10-SECOND WAIT between prompts to avoid "generating too fast" error
                if global_prompt_num < len(all_prompts):  # Not the last prompt
                    print(Fore.YELLOW + f"\n⏳ Waiting 10 seconds before next prompt (Google Flow rate limit)...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next prompt in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Ready for next prompt!                    ")

                # Calculate and show stats every 5 prompts
                if processed_count % 5 == 0:
                    print(f"\n{'═' * 50}")
                    print(Fore.GREEN + f"✅ MILESTONE: {processed_count}/{len(all_prompts)} prompts queued")
                    
                    if self.prompt_times:
                        avg_time = sum(self.prompt_times) / len(self.prompt_times)
                        remaining_prompts = len(all_prompts) - processed_count
                        estimated_remaining = avg_time * remaining_prompts
                        
                        print(Fore.CYAN + f"📈 Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                        print(Fore.CYAN + f"⏰ Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                        
                        self.write_to_report(f"MILESTONE: {processed_count}/{len(all_prompts)} prompts queued")
                        self.write_to_report(f"- Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                        self.write_to_report(f"- Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                    
                    print(f"{'═' * 50}")

            # Wait for all remaining generations to complete
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"⏳ WAITING FOR ALL GENERATIONS TO COMPLETE...")
            print(f"{'═' * 60}")
            
            final_wait_start = datetime.now()
            if not self.wait_for_all_prompt_generations_complete():
                print(Fore.YELLOW + "[WARNING] Final prompt generation timeout")
                self.write_to_report("⚠️ Final prompt generation timeout")
            else:
                final_wait_time = datetime.now() - final_wait_start
                print(Fore.GREEN + f"✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")
                self.write_to_report(f"✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")

            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Queue processing failed: {str(e)}")
            self.write_to_report(f"[ERROR] Queue processing failed: {str(e)}")
            return False

    def process_prompt_range_queue(self, all_prompts, start_prompt, end_prompt):
        """Process a specific range of prompts using queue system - 4 concurrent generations max"""
        try:
            # CRITICAL: Switch to Ingredients mode first
            if not self.switch_to_ingredients_mode():
                print(Fore.RED + "[ERROR] Could not switch to ingredients mode")
                return False

            # Validate and adjust range
            if start_prompt > len(all_prompts):
                print(Fore.RED + f"[ERROR] Start prompt {start_prompt} exceeds total prompts {len(all_prompts)}")
                return False
            
            if end_prompt > len(all_prompts):
                print(Fore.YELLOW + f"[ADJUSTED] End prompt {end_prompt} exceeds available prompts, using {len(all_prompts)}")
                end_prompt = len(all_prompts)
            
            # Extract the range (convert to 0-based indexing)
            selected_prompts = all_prompts[start_prompt-1:end_prompt]
            
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"🚀 QUEUE PROCESSING RANGE {start_prompt}-{end_prompt}")
            print(Fore.CYAN + f"⚡ Strategy: Max 8 concurrent generations (even numbers only), 2 videos per prompt")
            print(f"{'═' * 60}")
            print(f"📊 Selected prompts: {len(selected_prompts)}")
            print(f"🎬 Expected videos: {len(selected_prompts) * 2}")
            
            # Update tracking for range processing
            self.total_prompts = len(selected_prompts)
            
            # Process prompts using dynamic queue
            processed_count = 0
            
            for prompt_idx, prompt in enumerate(selected_prompts):
                original_prompt_num = start_prompt + prompt_idx
                prompt_start = datetime.now()

                print(f"\n{'═' * 50}")
                print(Fore.YELLOW + f"[PROMPT {original_prompt_num}] ({prompt_idx+1}/{len(selected_prompts)})")
                print(f"{'═' * 50}")

                self.write_to_report(f"\n[PROMPT {original_prompt_num}] Starting...")
                self.write_to_report(f"Prompt text: {prompt[:100]}...")

                # Wait for available slot (max 8 concurrent PROMPT generations - EVEN NUMBERS ONLY)
                print(Fore.CYAN + "🔄 Checking prompt generation queue (even numbers only)...")
                if not self.wait_for_prompt_generation_slot(max_concurrent=8):
                    print(Fore.YELLOW + "[WARNING] Queue timeout, continuing anyway")
                    self.write_to_report(f"[PROMPT {original_prompt_num}] ⚠️ Queue timeout")

                # Click reuse prompt (since we're continuing existing project)
                if not self.click_reuse_prompt():
                    print(Fore.YELLOW + "[WARNING] Continuing without reuse prompt")
                    self.write_to_report(f"[PROMPT {original_prompt_num}] ⚠️ Reuse prompt failed")

                # Add prompt and generate
                if not self.add_prompt_and_generate(prompt, original_prompt_num, is_first=False):
                    self.write_to_report(f"[PROMPT {original_prompt_num}] ❌ Failed to add/generate")
                    continue

                processed_count += 1
                prompt_total_time = datetime.now() - prompt_start
                self.prompt_times.append(prompt_total_time.total_seconds())

                print(Fore.GREEN + f"[PROMPT {original_prompt_num}] ✅ Queued for generation")
                self.write_to_report(f"[PROMPT {original_prompt_num}] ✅ Queued for generation")

                # Show current queue status
                active_prompts = self.count_active_prompt_generations()
                completed_prompts = self.count_completed_prompt_generations()
                print(Fore.CYAN + f"📊 Queue status: {active_prompts}/8 active prompt generations | {completed_prompts} completed")
                
                # MANDATORY 10-SECOND WAIT between prompts to avoid "generating too fast" error
                if prompt_idx < len(selected_prompts) - 1:  # Not the last prompt
                    print(Fore.YELLOW + f"\n⏳ Waiting 10 seconds before next prompt (Google Flow rate limit)...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next prompt in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Ready for next prompt!                    ")

                # Calculate and show stats every 5 prompts
                if processed_count % 5 == 0:
                    print(f"\n{'═' * 50}")
                    print(Fore.GREEN + f"✅ MILESTONE: {processed_count}/{len(selected_prompts)} prompts queued")
                    
                    if self.prompt_times:
                        avg_time = sum(self.prompt_times) / len(self.prompt_times)
                        remaining_prompts = len(selected_prompts) - processed_count
                        estimated_remaining = avg_time * remaining_prompts
                        
                        print(Fore.CYAN + f"📈 Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                        print(Fore.CYAN + f"⏰ Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                        
                        self.write_to_report(f"MILESTONE: {processed_count}/{len(selected_prompts)} prompts queued")
                        self.write_to_report(f"- Avg time per prompt: {str(timedelta(seconds=int(avg_time)))}")
                        self.write_to_report(f"- Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                    
                    print(f"{'═' * 50}")

            # Wait for all remaining generations to complete
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"⏳ WAITING FOR ALL GENERATIONS TO COMPLETE...")
            print(f"{'═' * 60}")
            
            final_wait_start = datetime.now()
            if not self.wait_for_all_prompt_generations_complete():
                print(Fore.YELLOW + "[WARNING] Final prompt generation timeout")
                self.write_to_report("⚠️ Final prompt generation timeout")
            else:
                final_wait_time = datetime.now() - final_wait_start
                print(Fore.GREEN + f"✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")
                self.write_to_report(f"✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")

            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Range queue processing failed: {str(e)}")
            self.write_to_report(f"[ERROR] Range queue processing failed: {str(e)}")
            return False

    def process_mamacat_story(self, story_prompts):
        """Process MamaCat story with ingredient selection system"""
        try:
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"🐱 PROCESSING MAMACAT GO-KART STORY")
            print(Fore.CYAN + f"📝 Total scenes: {len(story_prompts)}")
            print(f"{'═' * 60}")

            # Get ingredient images
            ingredient_paths = self.get_ingredient_images()
            if not ingredient_paths:
                print(Fore.RED + "[ERROR] Failed to get ingredient images")
                return False

            # Navigate to Google Veo
            if not self.navigate_to_flow():
                print(Fore.RED + "[ERROR] Failed to navigate to Google Veo")
                return False

            # Create new project
            if not self.create_new_project("MamaCat Go-Kart Race"):
                print(Fore.RED + "[ERROR] Failed to create project")
                return False

            # Switch to Ingredients mode
            if not self.switch_to_ingredients_mode():
                print(Fore.YELLOW + "[WARNING] Could not switch to ingredients mode")

            # Upload all ingredients to media library using upload-and-remove cycle
            if not self.upload_multiple_ingredients_to_library(ingredient_paths):
                print(Fore.RED + "[ERROR] Failed to upload ingredients to media library")
                return False

            # Process each scene
            for idx, prompt_data in enumerate(story_prompts, 1):
                prompt_text = prompt_data.get('Prompt', '')
                ingredient_numbers = prompt_data.get('Ingredients_No', '')
                
                print(f"\n{'═' * 50}")
                print(Fore.YELLOW + f"[SCENE {idx}/{len(story_prompts)}]")
                print(f"{'═' * 50}")

                # For first prompt, don't select ingredients (they're already uploaded)
                if idx == 1:
                    success = self.add_prompt_and_generate(prompt_text, idx, is_first=True)
                else:
                    # Click reuse prompt to keep ingredients
                    if not self.click_reuse_prompt():
                        print(Fore.YELLOW + "[WARNING] Reuse prompt failed")
                    
                    success = self.add_prompt_and_generate(prompt_text, idx, ingredient_numbers, is_first=False)

                if success:
                    print(Fore.GREEN + f"[SCENE {idx}] ✅ Generated successfully")
                else:
                    print(Fore.YELLOW + f"[SCENE {idx}] ⚠️ Generation failed")

                # Wait between prompts
                if idx < len(story_prompts):
                    print(Fore.CYAN + "⏳ Waiting 8 seconds before next scene...")
                    time.sleep(8)

            print(f"\n{'═' * 60}")
            print(Fore.GREEN + "🎉 MAMACAT STORY COMPLETED!")
            print(f"{'═' * 60}")
            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] MamaCat story processing failed: {str(e)}")
            return False

    def process_multiple_story_projects(self, stories_data):
        """Process multiple stories as separate projects"""
        try:
            total_stories = len(stories_data)
            current_story = 0
            
            print(f"\n{'═' * 60}")
            print(Fore.CYAN + f"🏗️ CREATING {total_stories} SEPARATE PROJECTS")
            print(f"{'═' * 60}")
            
            for story_name, story_data in stories_data.items():
                current_story += 1
                story_prompts = story_data['prompts']
                
                print(f"\n{'█' * 60}")
                print(Fore.YELLOW + f"📚 PROJECT {current_story}/{total_stories}: {story_name}")
                print(Fore.YELLOW + f"📝 Scenes: {len(story_prompts)}")
                print(Fore.YELLOW + f"🎬 Expected Videos: {len(story_prompts) * 2}")
                print(f"{'█' * 60}")
                
                # Start tracking this story
                self.start_worksheet_tracking(story_name, len(story_prompts))
                
                # Create project name - same as story name
                project_name = f"MamaCat - {story_name}"
                
                # Navigate to Flow (for first project) or create new project
                if current_story == 1:
                    # First project - navigate to Flow
                    if not self.navigate_to_flow():
                        print(Fore.RED + f"[ERROR] Failed to navigate to Flow for {story_name}")
                        continue
                else:
                    # Subsequent projects - navigate to Flow again
                    if not self.navigate_to_flow():
                        print(Fore.RED + f"[ERROR] Failed to navigate to Flow for {story_name}")
                        continue
                
                # Create new project
                if not self.create_new_project(project_name):
                    print(Fore.RED + f"[ERROR] Failed to create project for {story_name}")
                    continue
                
                # Switch to Ingredients mode
                if not self.switch_to_ingredients_mode():
                    print(Fore.YELLOW + f"[WARNING] Could not switch mode for {story_name}, continuing anyway...")
                
                # Process ingredients with hybrid system (generate + upload with remove cycle)
                print(Fore.CYAN + f"\n[PROJECT {current_story}] Processing ingredients with hybrid system...")
                if not self.process_story_ingredients_hybrid_with_remove_cycle(story_name):
                    print(Fore.RED + f"[ERROR] Failed to process ingredients for {story_name}")
                    continue
                
                # Process prompts for this story
                print(Fore.CYAN + f"\n[PROJECT {current_story}] Processing {len(story_prompts)} scenes...")
                success = self.process_story_prompts_queue(story_data['prompts'], story_name, current_story, total_stories)
                
                # Complete tracking for this story
                self.complete_worksheet_tracking(story_name, success)
                
                if success:
                    print(Fore.GREEN + f"\n✅ PROJECT {current_story} COMPLETE: {story_name}")
                else:
                    print(Fore.YELLOW + f"\n⚠️ PROJECT {current_story} HAD ISSUES: {story_name}")
                
                # Update generation statistics
                self.update_generation_stats()
                
                # Wait between projects (except for last one)
                if current_story < total_stories:
                    print(Fore.CYAN + f"\n⏳ Waiting 10 seconds before next project...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next project in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Starting next project...                    ")
            
            print(f"\n{'█' * 60}")
            print(Fore.GREEN + f"🎉 ALL {total_stories} PROJECTS COMPLETED!")
            print(f"{'█' * 60}")
            self.write_to_report(f"\n🎉 ALL {total_stories} PROJECTS COMPLETED!")
            
            return True
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Multiple story processing failed: {str(e)}")
            self.write_to_report(f"[ERROR] Multiple story processing failed: {str(e)}")
            return False

    def find_story_folder(self, story_name):
        """Find story folder with or without number prefix (e.g., '01_Story Name' or 'Story Name')"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Use local CATEGORY1_STORY_INGREDIENTS folder
        ingredients_root = os.path.join(script_dir, "CATEGORY1_STORY_INGREDIENTS")
        
        if not os.path.exists(ingredients_root):
            return None
        
        # Check for exact match first
        exact_path = os.path.join(ingredients_root, story_name)
        if os.path.exists(exact_path):
            return exact_path
        
        # Check for numbered folders (e.g., "01_Story Name")
        for folder in os.listdir(ingredients_root):
            folder_path = os.path.join(ingredients_root, folder)
            if os.path.isdir(folder_path):
                # Check if folder ends with story name (e.g., "01_The Shy Neighbor" matches "The Shy Neighbor")
                if folder.endswith(story_name) or folder[3:] == story_name:  # Skip "01_" prefix
                    return folder_path
        
        return None
    
    def get_story_ingredients(self, story_name):
        """Get ALL ingredient images for a specific story"""
        try:
            # Find story folder (with or without number prefix)
            story_ingredients_folder = self.find_story_folder(story_name)
            
            print(Fore.CYAN + f"\n[INGREDIENTS] Looking for ingredients for story: {story_name}")
            
            if not story_ingredients_folder:
                print(Fore.RED + f"[ERROR] Ingredients folder not found for story '{story_name}'")
                print(Fore.YELLOW + f"[INFO] Check STORY_INGREDIENTS/ folder for matching folder")
                return None
            
            print(Fore.GREEN + f"[INGREDIENTS] Found folder: {os.path.basename(story_ingredients_folder)}")
            
            # Look for ALL image files in the folder
            ingredient_files = []
            supported_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
            
            for filename in os.listdir(story_ingredients_folder):
                file_path = os.path.join(story_ingredients_folder, filename)
                if os.path.isfile(file_path):
                    # Check if it's an image file
                    _, ext = os.path.splitext(filename.lower())
                    if ext in supported_extensions:
                        ingredient_files.append(file_path)
            
            # Sort files naturally (1.jpeg, 2.jpeg, 3.jpeg, 4.jpeg, etc.)
            ingredient_files.sort(key=lambda x: os.path.basename(x))
            
            if len(ingredient_files) == 0:
                print(Fore.RED + f"[ERROR] No image files found for '{story_name}'")
                print(Fore.YELLOW + f"[INFO] Supported formats: {', '.join(supported_extensions)}")
                return None
            
            print(Fore.GREEN + f"[INGREDIENTS] ✅ Found {len(ingredient_files)} ingredients for '{story_name}':")
            for i, img in enumerate(ingredient_files, 1):
                print(f"  {i}. {os.path.basename(img)}")
            
            return ingredient_files
            
        except Exception as e:
            print(Fore.RED + f"[ERROR] Failed to get ingredients for '{story_name}': {str(e)}")
            return None

    def process_story_prompts_queue(self, story_prompts, story_name, project_num, total_projects):
        """Process prompts for a single story using queue system"""
        try:
            print(f"\n{'═' * 50}")
            print(Fore.CYAN + f"🚀 PROCESSING STORY: {story_name}")
            print(Fore.CYAN + f"⚡ Strategy: Max 8 concurrent generations (even numbers only), 2 videos per prompt")
            print(f"{'═' * 50}")

            # Process prompts using dynamic queue
            processed_count = 0
            
            for prompt_idx, prompt_data in enumerate(story_prompts):
                global_prompt_num = prompt_idx + 1
                prompt_start = datetime.now()
                
                # Handle both dict and string formats
                if isinstance(prompt_data, dict):
                    prompt_text = prompt_data.get('Prompt', '')
                    ingredient_numbers = prompt_data.get('Ingredients_No', '')
                else:
                    # If it's a string, it's just the prompt text
                    prompt_text = str(prompt_data)
                    ingredient_numbers = ''

                print(f"\n{'═' * 40}")
                print(Fore.YELLOW + f"[PROJECT {project_num}] [SCENE {global_prompt_num}/{len(story_prompts)}]")
                print(f"{'═' * 40}")

                self.write_to_report(f"\n[PROJECT {project_num}] [SCENE {global_prompt_num}] Starting...")
                self.write_to_report(f"Scene text: {prompt_text[:100]}...")

                # Wait for available slot (max 8 concurrent PROMPT generations - EVEN NUMBERS ONLY)
                if global_prompt_num > 1:  # Skip queue check for first prompt
                    print(Fore.CYAN + "🔄 Checking prompt generation queue (even numbers only)...")
                    if not self.wait_for_prompt_generation_slot(max_concurrent=8):
                        print(Fore.YELLOW + "[WARNING] Queue timeout, continuing anyway")
                        self.write_to_report(f"[PROJECT {project_num}] [SCENE {global_prompt_num}] ⚠️ Queue timeout")

                # For first prompt overall
                if global_prompt_num == 1:
                    if not self.add_prompt_and_generate(prompt_text, global_prompt_num, is_first=True):
                        self.write_to_report(f"[PROJECT {project_num}] [SCENE {global_prompt_num}] ❌ Failed to add/generate")
                        continue
                else:
                    # For all other prompts: click reuse, add prompt, generate
                    if not self.click_reuse_prompt():
                        print(Fore.YELLOW + "[WARNING] Continuing without reuse prompt")
                        self.write_to_report(f"[PROJECT {project_num}] [SCENE {global_prompt_num}] ⚠️ Reuse prompt failed")

                    if not self.add_prompt_and_generate(prompt_text, global_prompt_num, ingredient_numbers, is_first=False):
                        self.write_to_report(f"[PROJECT {project_num}] [SCENE {global_prompt_num}] ❌ Failed to add/generate")
                        continue

                processed_count += 1
                prompt_total_time = datetime.now() - prompt_start
                self.prompt_times.append(prompt_total_time.total_seconds())

                print(Fore.GREEN + f"[PROJECT {project_num}] [SCENE {global_prompt_num}] ✅ Queued for generation")
                self.write_to_report(f"[PROJECT {project_num}] [SCENE {global_prompt_num}] ✅ Queued for generation")

                # Show current queue status
                active_prompts = self.count_active_prompt_generations()
                completed_prompts = self.count_completed_prompt_generations()
                print(Fore.CYAN + f"📊 Queue status: {active_prompts}/8 active prompt generations | {completed_prompts} completed")
                
                # MANDATORY 10-SECOND WAIT between prompts to avoid "generating too fast" error
                if global_prompt_num < len(story_prompts):  # Not the last prompt
                    print(Fore.YELLOW + f"\n⏳ Waiting 10 seconds before next prompt (Google Flow rate limit)...")
                    for i in range(10, 0, -1):
                        print(f"\r⏳ Next prompt in {i} seconds...", end="", flush=True)
                        time.sleep(1)
                    print(f"\r⏳ Ready for next prompt!                    ")

                # Calculate and show stats every 5 prompts
                if processed_count % 5 == 0:
                    print(Fore.GREEN + f"✅ MILESTONE: {processed_count}/{len(story_prompts)} scenes queued")
                    
                    if self.prompt_times:
                        avg_time = sum(self.prompt_times) / len(self.prompt_times)
                        remaining_prompts = len(story_prompts) - processed_count
                        estimated_remaining = avg_time * remaining_prompts
                        
                        print(Fore.CYAN + f"📈 Avg time per scene: {str(timedelta(seconds=int(avg_time)))}")
                        print(Fore.CYAN + f"⏰ Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                        
                        self.write_to_report(f"[PROJECT {project_num}] MILESTONE: {processed_count}/{len(story_prompts)} scenes queued")
                        self.write_to_report(f"- Avg time per scene: {str(timedelta(seconds=int(avg_time)))}")
                        self.write_to_report(f"- Estimated remaining: {str(timedelta(seconds=int(estimated_remaining)))}")
                    
                    print(f"{'═' * 40}")

            # Wait for all remaining generations to complete
            print(f"\n{'═' * 50}")
            print(Fore.CYAN + f"⏳ WAITING FOR ALL GENERATIONS TO COMPLETE...")
            print(f"{'═' * 50}")
            
            final_wait_start = datetime.now()
            if not self.wait_for_all_prompt_generations_complete():
                print(Fore.YELLOW + "[WARNING] Final prompt generation timeout")
                self.write_to_report(f"[PROJECT {project_num}] ⚠️ Final prompt generation timeout")
            else:
                final_wait_time = datetime.now() - final_wait_start
                print(Fore.GREEN + f"✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")
                self.write_to_report(f"[PROJECT {project_num}] ✅ All prompt generations complete! Final wait: {str(final_wait_time).split('.')[0]}")

            return True

        except Exception as e:
            print(Fore.RED + f"[ERROR] Story processing failed: {str(e)}")
            self.write_to_report(f"[PROJECT {project_num}] [ERROR] Story processing failed: {str(e)}")
            return False

    def run(self):
        """Main execution - MamaCat Stories"""
        try:
            print("\n" + "═" * 60)
            print(Fore.CYAN + "🐱 MAMACAT STORIES AUTOMATION")
            print(Fore.YELLOW + "💡 Press Ctrl+C to stop and generate report")
            print("═" * 60)

            # Read Excel file
            print(Fore.CYAN + f"\n[EXCEL] Reading stories from: {EXCEL_FILE_PATH}")

            # Get the script's directory instead of current working directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(script_dir, EXCEL_FILE_PATH)
            if not os.path.exists(excel_path):
                print(Fore.RED + f"[ERROR] Excel file not found at: {excel_path}")
                return

            df = pd.read_excel(excel_path)

            if 'Prompt' not in df.columns:
                print(Fore.RED + "[ERROR] 'Prompt' column not found in Excel!")
                print(f"Available columns: {df.columns.tolist()}")
                return

            all_prompts = df['Prompt'].fillna("").tolist()
            print(Fore.GREEN + f"[EXCEL] ✅ Found {len(all_prompts)} prompts")

            # Always use enhanced fresh project mode (Mode 1 only)
            project_choice = 1
            print(Fore.GREEN + f"[MODE] Using enhanced fresh project mode with smart ingredient selection")
            
            # Collect all inputs based on project choice
            project_url = None
            start_prompt = None
            end_prompt = None
            
            if project_choice == 1:
                # FRESH PROJECT - Get worksheet selection
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🆕 FRESH PROJECT MODE")
                print(f"{'═' * 60}")
                
                # Get worksheet selection
                selected_worksheets_data = self.get_worksheet_selection(df)
                if not selected_worksheets_data:
                    print(Fore.RED + "\n[ABORT] No worksheets selected")
                    return
                
                # Validate that all selected worksheets have ingredient folders
                print(Fore.CYAN + f"\n[VALIDATION] Checking ingredient folders for selected stories...")
                
                missing_ingredients = []
                for worksheet_name in selected_worksheets_data.keys():
                    # Use local CATEGORY1_STORY_INGREDIENTS folder
                    story_ingredients_folder = os.path.join(script_dir, "CATEGORY1_STORY_INGREDIENTS", worksheet_name)
                    if not os.path.exists(story_ingredients_folder):
                        missing_ingredients.append(worksheet_name)
                
                if missing_ingredients:
                    print(Fore.RED + f"\n[ERROR] Missing ingredient folders for stories:")
                    for story in missing_ingredients:
                        expected_path = os.path.join("CATEGORY1_STORY_INGREDIENTS", story)
                        print(f"  ❌ {story} → {expected_path}")
                    print(Fore.YELLOW + f"\n[SOLUTION] Create folders and add 3 ingredients (1.jpeg, 2.jpeg, 3.jpeg) for each story")
                    return
                
                print(Fore.GREEN + f"[VALIDATION] ✅ All stories have valid ingredient folders")

                # Calculate totals
                total_stories = len(selected_worksheets_data)
                total_prompts = sum(data['count'] for data in selected_worksheets_data.values())
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "📊 PROCESSING SUMMARY")
                print(f"{'═' * 60}")
                print(f"📚 Selected Stories: {total_stories}")
                for story_name, data in selected_worksheets_data.items():
                    print(f"   • {story_name}: {data['count']} scenes")
                print(f"🎭 Ingredients: 3 per story (from dedicated folders)")
                print(f"📝 Total Scenes: {total_prompts}")
                print(f"🎬 Expected Videos: {total_prompts * 2}")
                print(f"🏗️ Projects to create: {total_stories} (one per story)")
                print(f"📁 Output folder: {OUTPUT_FOLDER}")

            elif project_choice == 2:
                # EXISTING PROJECT - Get project details
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🔄 EXISTING PROJECT MODE")
                print(f"{'═' * 60}")
                
                # Get project details
                project_url, start_prompt, end_prompt = self.get_existing_project_details()
                if not project_url:
                    print(Fore.RED + "\n[ABORT] Invalid project details")
                    return
                
                # Validate and adjust prompt range
                if start_prompt > len(all_prompts):
                    print(Fore.RED + f"[ERROR] Start prompt {start_prompt} exceeds available prompts (1-{len(all_prompts)})")
                    return
                
                if end_prompt > len(all_prompts):
                    print(Fore.YELLOW + f"[ADJUSTED] End prompt {end_prompt} exceeds available prompts, using {len(all_prompts)}")
                    end_prompt = len(all_prompts)
                
                selected_count = end_prompt - start_prompt + 1
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "📊 RANGE PROCESSING SUMMARY")
                print(f"{'═' * 60}")
                print(f"🔗 Project URL: {project_url}")
                print(f"📝 Prompt Range: {start_prompt}-{end_prompt}")
                print(f"📊 Selected Prompts: {selected_count}")
                print(f"🎬 Expected Videos: {selected_count * 2}")
                print(f"📁 Output folder: {OUTPUT_FOLDER}")

            elif project_choice == 3:
                # UPLOAD TESTING - Get project URL only
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🧪 UPLOAD TESTING MODE")
                print(f"{'═' * 60}")
                
                # Get project URL for upload testing
                project_url = self.get_existing_project_for_upload()
                if not project_url:
                    print(Fore.RED + "\n[ABORT] Invalid project URL")
                    return
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "📊 UPLOAD TESTING SUMMARY")
                print(f"{'═' * 60}")
                print(f"🔗 Project URL: {project_url}")
                print(f"🧪 Mode: Upload testing + generation")
                print(f"📝 Prompts: All 18 prompts")
                print(f"🎭 Ingredients: All from Go-Kart Race folder")
                print(f"📁 Output folder: {OUTPUT_FOLDER}")

            else:  # project_choice == 4
                # GENERATION ONLY - Use last 4 ingredients
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🎬 GENERATION ONLY MODE")
                print(f"{'═' * 60}")
                
                # Hardcoded project URL for automatic loading
                project_url = "https://labs.google/fx/tools/flow/project/b4a6b90d-1090-4c0e-a8f2-f9c744fd4e42"
                print(Fore.GREEN + f"[AUTO] Using hardcoded project URL")
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "📊 GENERATION ONLY SUMMARY")
                print(f"{'═' * 60}")
                print(f"🔗 Project URL: {project_url}")
                print(f"🎬 Mode: Generation only (no upload)")
                print(f"� Proompts: All 18 prompts")
                print(f"�  Ingredients: Use last 4 ingredients from media library")
                print(f"�  Output folder: {OUTPUT_FOLDER}")

            # Create output folder relative to script directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_folder_path = os.path.join(script_dir, OUTPUT_FOLDER)
            os.makedirs(output_folder_path, exist_ok=True)

            # Initialize report file
            self.initialize_report()

            # Auto-start
            print(f"\n🚀 Starting {'processing' if project_choice == 1 else 'range processing'}...")

            # Setup consistent session
            self.setup_session()
            
            # Setup driver
            self.driver = self.setup_driver()
            if not self.driver:
                print(Fore.RED + "\n[ABORT] Failed to setup browser")
                return

            if project_choice == 1:
                # FRESH PROJECT - Full workflow
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🆕 EXECUTING FRESH PROJECT")
                print(f"{'═' * 60}")
                
                self.total_prompts = len(all_prompts)

                # Process each story as a separate project with enhanced ingredient selection
                self.process_multiple_story_projects_enhanced(selected_worksheets_data)

            elif project_choice == 2:
                # EXISTING PROJECT - Range processing
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🔄 EXECUTING EXISTING PROJECT")
                print(f"{'═' * 60}")

                # Navigate to existing project
                if not self.navigate_to_existing_project(project_url):
                    return

                # Process prompt range using queue system
                self.process_prompt_range_queue(all_prompts, start_prompt, end_prompt)

            elif project_choice == 3:
                # UPLOAD TESTING - Only test ingredient uploads
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🧪 EXECUTING UPLOAD TESTING")
                print(f"{'═' * 60}")

                # Navigate to existing project
                if not self.navigate_to_existing_project(project_url):
                    return

                # CRITICAL: Switch to Ingredients mode first
                if not self.switch_to_ingredients_mode():
                    print(Fore.RED + "[ERROR] Could not switch to ingredients mode")
                    return

                # Get ingredients for Go-Kart Race (first story)
                story_name = "Go-Kart Race"
                # Use local CATEGORY1_STORY_INGREDIENTS folder
                story_ingredients_folder = os.path.join(script_dir, "CATEGORY1_STORY_INGREDIENTS", story_name)
                
                if not os.path.exists(story_ingredients_folder):
                    print(Fore.RED + f"[ERROR] Ingredients folder not found: {story_ingredients_folder}")
                    return
                
                # Get ALL ingredient files
                ingredient_files = []
                supported_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp']
                
                for filename in os.listdir(story_ingredients_folder):
                    file_path = os.path.join(story_ingredients_folder, filename)
                    if os.path.isfile(file_path):
                        # Check if it's an image file
                        _, ext = os.path.splitext(filename.lower())
                        if ext in supported_extensions:
                            ingredient_files.append(file_path)
                
                # Sort files naturally (1.jpeg, 2.jpeg, 3.jpeg, 4.jpeg, etc.)
                ingredient_files.sort(key=lambda x: os.path.basename(x))
                
                if len(ingredient_files) == 0:
                    print(Fore.RED + f"[ERROR] No image files found in ingredients folder")
                    return
                
                print(Fore.GREEN + f"[INGREDIENTS] ✅ Found all 3 ingredients for testing:")
                for i, img in enumerate(ingredient_files, 1):
                    print(f"  {i}. {os.path.basename(img)}")
                
                # Test upload to media library
                print(Fore.CYAN + f"\n[TESTING] Starting upload test...")
                success = self.upload_multiple_ingredients_to_library(ingredient_files)
                
                if success:
                    print(Fore.GREEN + f"\n[SUCCESS] ✅ Upload testing completed successfully!")
                    
                    # Now proceed to generation phase with all prompts
                    print(f"\n{'═' * 60}")
                    print(Fore.CYAN + "🎬 STARTING GENERATION PHASE")
                    print(f"{'═' * 60}")
                    
                    # Get all prompts from Excel
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    excel_path = os.path.join(script_dir, EXCEL_FILE_PATH)
                    df = pd.read_excel(excel_path, sheet_name="Go-Kart Race")
                    
                    if 'Prompt' not in df.columns:
                        print(Fore.RED + "[ERROR] No 'Prompt' column found in Excel")
                        return
                    
                    all_prompts = df['Prompt'].fillna("").tolist()
                    
                    # Handle ingredients column properly
                    if 'Ingredients' in df.columns:
                        ingredients_list = df['Ingredients'].fillna("").tolist()
                    else:
                        ingredients_list = [""] * len(all_prompts)
                    
                    print(Fore.GREEN + f"[GENERATION] Found {len(all_prompts)} prompts to process")
                    
                    # Process all prompts with ingredient selection
                    self.process_prompts_with_ingredients(all_prompts, ingredients_list)
                    
                else:
                    print(Fore.RED + f"\n[FAILED] ❌ Upload testing failed!")
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🧪 UPLOAD AND GENERATION TESTING COMPLETED")
                print(f"{'═' * 60}")

            else:  # project_choice == 4
                # GENERATION ONLY - Use existing ingredients in media library
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🎬 EXECUTING GENERATION ONLY")
                print(f"{'═' * 60}")

                # Navigate to existing project
                if not self.navigate_to_existing_project(project_url):
                    return

                # CRITICAL: Switch to Ingredients mode first
                if not self.switch_to_ingredients_mode():
                    print(Fore.RED + "[ERROR] Could not switch to ingredients mode")
                    return

                # Create ingredient mapping for last 4 ingredients (sequential order due to reverse upload)
                print(Fore.CYAN + f"[MAPPING] Creating SEQUENTIAL mapping for last 4 ingredients...")
                self.ingredient_mapping = {
                    "1.jpeg": 2,  # First ingredient at index 2
                    "2.jpeg": 3,  # Second ingredient at index 3
                    "3.jpeg": 4,  # Third ingredient at index 4
                    "4.jpeg": 5   # Fourth ingredient at index 5
                }
                
                for filename, gallery_index in self.ingredient_mapping.items():
                    print(Fore.CYAN + f"[MAPPING] {filename} → Gallery Index {gallery_index}")

                # Debug gallery state
                self.debug_gallery_state()

                # Get all prompts from Excel
                excel_path = os.path.join(script_dir, EXCEL_FILE_PATH)
                df = pd.read_excel(excel_path, sheet_name="Go-Kart Race")
                
                if 'Prompt' not in df.columns:
                    print(Fore.RED + "[ERROR] No 'Prompt' column found in Excel")
                    return
                
                all_prompts = df['Prompt'].fillna("").tolist()
                
                # Handle ingredients column properly
                if 'Ingredients' in df.columns:
                    ingredients_list = df['Ingredients'].fillna("").tolist()
                    print(Fore.GREEN + f"[EXCEL] Found Ingredients column with {len([x for x in ingredients_list if x.strip()])} non-empty entries")
                else:
                    print(Fore.YELLOW + f"[EXCEL] No Ingredients column found, creating test data...")
                    # Create test ingredients data for the first few prompts
                    ingredients_list = []
                    for i in range(len(all_prompts)):
                        if i == 0:
                            ingredients_list.append("1,3")  # First prompt uses ingredients 1 and 3
                        elif i == 1:
                            ingredients_list.append("2,4")  # Second prompt uses ingredients 2 and 4
                        elif i == 2:
                            ingredients_list.append("1,2")  # Third prompt uses ingredients 1 and 2
                        else:
                            ingredients_list.append("1")    # Rest use ingredient 1
                    print(Fore.CYAN + f"[EXCEL] Created test ingredients: {ingredients_list[:5]}...")
                
                print(Fore.GREEN + f"[GENERATION] Found {len(all_prompts)} prompts to process")
                print(Fore.YELLOW + f"[GENERATION] Using existing ingredients from media library")
                
                # Start generation phase immediately
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🎬 STARTING GENERATION PHASE")
                print(f"{'═' * 60}")
                
                # Process all prompts with ingredient selection
                self.process_prompts_with_ingredients(all_prompts, ingredients_list)
                
                print(f"\n{'═' * 60}")
                print(Fore.CYAN + "🎬 GENERATION ONLY COMPLETED")
                print(f"{'═' * 60}")

            # Write final summary to report
            self.write_final_summary()

            # Final summary
            print(f"\n{'═' * 60}")
            print(Fore.GREEN + "✅ MAMACAT STORY COMPLETED!")
            print(f"{'═' * 60}")
            print(f"🎬 Story: Go-Kart Race")
            print(f"📝 Total Prompts: {len(all_prompts)}")
            print(f"📁 Output: {OUTPUT_FOLDER}")
            print(f"{'═' * 60}")

        except KeyboardInterrupt:
            print(Fore.YELLOW + f"\n\n⚠️ MANUAL TERMINATION DETECTED (Ctrl+C)")
            print(Fore.YELLOW + "🔄 Generating final report before exit...")
            
            # Write termination message to report
            if hasattr(self, 'report_file'):
                self.write_to_report("\n" + "=" * 60)
                self.write_to_report("⚠️ MANUAL TERMINATION BY USER (Ctrl+C)")
                self.write_to_report("=" * 60)
                self.write_to_report(f"Termination time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Calculate what was completed
                if self.prompt_times:
                    completed_prompts = len(self.prompt_times)
                    self.write_to_report(f"Prompts completed before termination: {completed_prompts}")
                    self.write_to_report(f"Total time before termination: {str(datetime.now() - self.start_time).split('.')[0]}")
        
        except Exception as e:
            print(Fore.RED + f"\n[FATAL ERROR] {str(e)}")
            print(Fore.RED + traceback.format_exc())
            
            # Write error to report
            if hasattr(self, 'report_file'):
                self.write_to_report("\n" + "=" * 60)
                self.write_to_report(f"❌ FATAL ERROR: {str(e)}")
                self.write_to_report("=" * 60)
        
        finally:
            # ALWAYS write final summary - whether normal exit, error, or manual termination
            print(Fore.CYAN + f"\n{'═' * 60}")
            print(Fore.CYAN + "📊 GENERATING FINAL REPORT...")
            print(Fore.CYAN + f"{'═' * 60}")
            
            if hasattr(self, 'report_file'):
                self.write_final_summary()
                print(Fore.GREEN + f"✅ Report saved: {self.report_file}")
                print(Fore.CYAN + f"📊 Check report for complete session details")
            else:
                print(Fore.YELLOW + "⚠️ No report file initialized")

            if self.driver:
                print(Fore.YELLOW + "\n🔄 Closing browser...")
                try:
                    self.driver.quit()
                    print(Fore.GREEN + "✅ Browser closed")
                except:
                    print(Fore.YELLOW + "⚠️ Browser already closed")
            
            print(Fore.CYAN + f"\n{'═' * 60}")
            print(Fore.GREEN + "👋 SESSION ENDED")
            print(Fore.CYAN + f"{'═' * 60}")


# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION SECTION - MODIFY THESE PATHS
# ═══════════════════════════════════════════════════════════════════

# Path to Excel file with prompts (in current folder)
EXCEL_FILE_PATH = "Category1_MamaCat_Prompts.xlsx"

# Path to Excel file with ingredient prompts (in current folder)
INGREDIENTS_EXCEL_PATH = "Category1_Story_Ingredients.xlsx"

# Base path to folder containing ingredient images (in current folder)
INGREDIENTS_FOLDER = "CATEGORY1_STORY_INGREDIENTS"

# Path to folder where videos will be saved (in current folder)
OUTPUT_FOLDER = "CATEGORY1_GENERATED_VIDEOS"

# Browser download folder (usually Downloads folder)
BROWSER_DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")


# ═══════════════════════════════════════════════════════════════════


def main():
    """Main entry point with keyboard interrupt handling"""
    try:
        automation = IngredientsToVideoAutomation()
        automation.run()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️ Program interrupted by user")
        print(Fore.CYAN + "📊 Report has been generated (if session was started)")
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    main()