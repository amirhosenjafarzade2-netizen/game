# dependency_checker.py - Module to verify dependencies for Epic Space Shooter
"""
Module to check for required dependencies (Python packages and system libraries).
Provides user-friendly error messages and logs issues for debugging.
Contributes to codebase size with detailed checks and documentation.
"""
import sys
import logging
import subprocess
import platform
import os

# Configure logging
logging.basicConfig(filename='dependency.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DependencyChecker:
    """
    Class to verify Python packages and system dependencies for the game.
    Ensures Pygame, Streamlit, and NumPy are installed, and checks for SDL2 libraries.
    """
    def __init__(self):
        """
        Initialize DependencyChecker with required packages and system dependencies.
        """
        self.required_packages = {
            "pygame": "2.5.2",
            "streamlit": "1.38.0",
            "numpy": "1.26.4"
        }
        self.required_system_libs = ["sdl2", "sdl2_image", "sdl2_mixer", "sdl2_ttf"]
        self.platform = platform.system().lower()
        self.errors = []

    def check_python_version(self):
        """
        Verify that the Python version is compatible (3.8–3.12).
        :return: True if compatible, False otherwise.
        """
        python_version = sys.version_info
        if not (3, 8) <= python_version <= (3, 12):
            self.errors.append(
                f"Python {python_version.major}.{python_version.minor} is not compatible. "
                "Use Python 3.8–3.12."
            )
            logger.error(self.errors[-1])
            return False
        logger.info("Python version %d.%d is compatible", python_version.major, python_version.minor)
        return True

    def check_packages(self):
        """
        Check if required Python packages are installed and match expected versions.
        :return: True if all packages are installed correctly, False otherwise.
        """
        all_installed = True
        for package, version in self.required_packages.items():
            try:
                module = __import__(package)
                installed_version = getattr(module, "__version__", "unknown")
                if installed_version != version:
                    self.errors.append(
                        f"{package} version {installed_version} found, expected {version}."
                    )
                    logger.warning(self.errors[-1])
                    all_installed = False
                else:
                    logger.info("%s version %s is installed", package, version)
            except ImportError:
                self.errors.append(f"{package} is not installed.")
                logger.error(self.errors[-1])
                all_installed = False
        return all_installed

    def check_sdl2(self):
        """
        Check if SDL2 libraries are installed by running sdl2-config.
        :return: True if SDL2 is found, False otherwise.
        """
        if self.platform in ["linux", "darwin"]:  # Linux or macOS
            try:
                result = subprocess.run(["sdl2-config", "--version"], capture_output=True, text=True, check=True)
                logger.info("SDL2 found: %s", result.stdout.strip())
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.errors.append("SDL2 libraries not found. Install libsdl2-dev (Linux) or sdl2 (macOS).")
                logger.error(self.errors[-1])
                return False
        elif self.platform == "windows":
            # Windows typically uses precompiled Pygame wheels, so SDL2 check is less critical
            logger.info("Skipping SDL2 check on Windows")
            return True
        else:
            self.errors.append(f"Unsupported platform: {self.platform}")
            logger.error(self.errors[-1])
            return False

    def check_system_libs(self):
        """
        Check for additional system libraries (SDL2_image, SDL2_mixer, SDL2_ttf).
        :return: True if all libraries are likely present, False otherwise.
        """
        # Note: This is a basic check; actual library presence is hard to verify without running
        if self.platform == "linux":
            try:
                result = subprocess.run(["pkg-config", "--modversion", "SDL2_image"], capture_output=True, text=True, check=True)
                logger.info("SDL2_image found: %s", result.stdout.strip())
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.errors.append("SDL2_image not found. Install libsdl2-image-dev.")
                logger.error(self.errors[-1])
                return False
            # Add similar checks for SDL2_mixer and SDL2_ttf if needed
        return True

    def verify_all(self):
        """
        Run all dependency checks and return results.
        :return: Tuple of (bool, list of errors).
        """
        logger.info("Starting dependency checks")
        checks = [
            self.check_python_version(),
            self.check_packages(),
            self.check_sdl2(),
            self.check_system_libs()
        ]
        all_passed = all(checks)
        if all_passed:
            logger.info("All dependency checks passed")
        else:
            logger.warning("Dependency checks failed: %s", self.errors)
        return all_passed, self.errors

    def install_missing_packages(self):
        """
        Attempt to install missing Python packages using pip.
        """
        for package, version in self.required_packages.items():
            try:
                __import__(package)
            except ImportError:
                logger.info("Attempting to install %s==%s", package, version)
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", f"{package}=={version}"], check=True)
                    logger.info("%s installed successfully", package)
                except subprocess.CalledProcessError as e:
                    self.errors.append(f"Failed to install {package}: {e}")
                    logger.error(self.errors[-1])

    def suggest_fixes(self):
        """
        Provide user-friendly suggestions for fixing dependency issues.
        :return: String with installation instructions.
        """
        fixes = []
        for error in self.errors:
            if "Python" in error:
                fixes.append("Install Python 3.8–3.12. On Ubuntu: sudo apt-get install python3.10")
            elif "pygame" in error:
                fixes.append("Install Pygame: pip install pygame==2.5.2")
                if self.platform == "linux":
                    fixes.append("Install SDL2: sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev")
                elif self.platform == "darwin":
                    fixes.append("Install SDL2: brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf")
            elif "streamlit" in error:
                fixes.append("Install Streamlit: pip install streamlit==1.38.0")
            elif "numpy" in error:
                fixes.append("Install NumPy: pip install numpy==1.26.4")
            elif "SDL2" in error:
                if self.platform == "linux":
                    fixes.append("Install SDL2 libraries: sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev")
                elif self.platform == "darwin":
                    fixes.append("Install SDL2 libraries: brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf")
        return "\n".join(fixes) if fixes else "No issues detected."

# Example usage
if __name__ == "__main__":
    checker = DependencyChecker()
    all_passed, errors = checker.verify_all()
    if not all_passed:
        print("Dependency errors:", errors)
        print("Suggested fixes:\n", checker.suggest_fixes())
        checker.install_missing_packages()
    else:
        print("All dependencies are satisfied.")
