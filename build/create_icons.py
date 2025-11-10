#!/usr/bin/env python3
"""
SPAMURAI Icon Generator
Creates .ico and .icns files from a source PNG image
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required libraries are installed"""
    try:
        from PIL import Image
        return True
    except ImportError:
        print("❌ Pillow is required but not installed")
        print("\nInstall with:")
        print("  pip install Pillow")
        return False

def create_windows_icon(source_image, output_path):
    """Create Windows .ico file"""
    from PIL import Image

    print(f"\n📦 Creating Windows icon: {output_path}")

    img = Image.open(source_image)

    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Create icon with multiple sizes
    # Windows ICO supports: 16, 24, 32, 48, 64, 128, 256
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (24, 24), (16, 16)]

    img.save(
        output_path,
        format='ICO',
        sizes=sizes
    )

    print(f"✅ Windows icon created: {output_path}")

def create_macos_icon(source_image, output_dir):
    """Create macOS .icns file using iconutil"""
    from PIL import Image

    print(f"\n🍎 Creating macOS icon...")

    # Create iconset directory
    iconset_dir = output_dir / 'SPAMURAI.iconset'
    iconset_dir.mkdir(exist_ok=True)

    img = Image.open(source_image)

    # Convert to RGBA if needed
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # macOS iconset requires these specific sizes
    sizes = [
        (16, 'icon_16x16.png'),
        (32, 'icon_16x16@2x.png'),
        (32, 'icon_32x32.png'),
        (64, 'icon_32x32@2x.png'),
        (128, 'icon_128x128.png'),
        (256, 'icon_128x128@2x.png'),
        (256, 'icon_256x256.png'),
        (512, 'icon_256x256@2x.png'),
        (512, 'icon_512x512.png'),
        (1024, 'icon_512x512@2x.png'),
    ]

    print("Creating iconset images...")
    for size, filename in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(iconset_dir / filename)
        print(f"  ✓ {filename}")

    # Convert iconset to icns using iconutil (macOS only)
    if sys.platform == 'darwin':
        import subprocess

        output_icns = output_dir / 'icon.icns'

        print(f"\nConverting to .icns...")
        result = subprocess.run(
            ['iconutil', '-c', 'icns', str(iconset_dir), '-o', str(output_icns)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"✅ macOS icon created: {output_icns}")

            # Clean up iconset directory
            import shutil
            shutil.rmtree(iconset_dir)
            print("🧹 Cleaned up temporary files")
            return True
        else:
            print(f"❌ Failed to create .icns: {result.stderr}")
            return False
    else:
        print("⚠️  iconutil not available (macOS only)")
        print(f"📁 Iconset created at: {iconset_dir}")
        print("   Upload to https://cloudconvert.com/png-to-icns to convert")
        return False

def create_simple_text_icon(output_dir):
    """Create a simple text-based icon with SPAMURAI branding"""
    from PIL import Image, ImageDraw, ImageFont

    print("\n🎨 Creating simple SPAMURAI icon...")

    # Create a 1024x1024 image with gradient background
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw gradient background (red to orange - SPAMURAI colors)
    for y in range(size):
        # RGB gradient from #D72638 to #F25C05
        r = int(215 + (242 - 215) * (y / size))
        g = int(38 + (92 - 38) * (y / size))
        b = int(56 + (5 - 56) * (y / size))
        draw.rectangle([(0, y), (size, y + 1)], fill=(r, g, b, 255))

    # Draw a circle border
    border_width = 60
    draw.ellipse(
        [(border_width, border_width), (size - border_width, size - border_width)],
        outline=(255, 255, 255, 200),
        width=border_width
    )

    # Try to add text (using default font if custom not available)
    try:
        # Try to use a system font
        font_size = 400
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()

        # Draw ninja emoji or S
        text = "🥷"
        try:
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size - text_width) // 2, (size - text_height) // 2 - 50)
            draw.text(position, text, fill=(255, 255, 255, 255), font=font)
        except:
            # Fallback to 'S' if emoji doesn't work
            text = "S"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size - text_width) // 2, (size - text_height) // 2 - 50)
            draw.text(position, text, fill=(255, 255, 255, 255), font=font)
    except Exception as e:
        print(f"⚠️  Could not add text: {e}")

    # Save as PNG
    temp_png = output_dir / 'icon_source.png'
    img.save(temp_png)
    print(f"✅ Created source image: {temp_png}")

    return temp_png

def main():
    """Main icon creation process"""
    print("="*60)
    print("🥷⚡ SPAMURAI Icon Generator")
    print("="*60)

    if not check_dependencies():
        sys.exit(1)

    build_dir = Path(__file__).parent

    # Check if source image exists
    source_image = None

    print("\nLooking for source image...")
    possible_sources = [
        build_dir / 'logo.png',
        build_dir / 'icon.png',
        build_dir / 'icon_source.png',
    ]

    for img_path in possible_sources:
        if img_path.exists():
            source_image = img_path
            print(f"✅ Found: {source_image}")
            break

    if not source_image:
        print("📝 No source image found. Creating a simple icon...")

        response = input("\nCreate a simple SPAMURAI-branded icon? (y/n): ").lower()
        if response == 'y':
            source_image = create_simple_text_icon(build_dir)
        else:
            print("\n📋 To create custom icons:")
            print("1. Create a 1024x1024 PNG logo")
            print("2. Save as build/logo.png")
            print("3. Run this script again")
            sys.exit(0)

    # Create icons
    print("\n" + "="*60)
    print("Creating icon files...")
    print("="*60)

    # Windows icon
    try:
        create_windows_icon(source_image, build_dir / 'icon.ico')
    except Exception as e:
        print(f"❌ Failed to create Windows icon: {e}")

    # macOS icon
    try:
        create_macos_icon(source_image, build_dir)
    except Exception as e:
        print(f"❌ Failed to create macOS icon: {e}")

    print("\n" + "="*60)
    print("✅ Icon generation complete!")
    print("="*60)
    print("\nGenerated files:")
    if (build_dir / 'icon.ico').exists():
        print(f"  📦 Windows: build/icon.ico")
    if (build_dir / 'icon.icns').exists():
        print(f"  🍎 macOS:   build/icon.icns")

    print("\nYou can now run the build script:")
    print("  cd build && python build.py")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
