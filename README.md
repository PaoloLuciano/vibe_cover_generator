# Vibe-Cover Generator

A tool to generate cool playlist covers by extracting and analyzing the "vibe" of images.

## Vision

The end goal is to create a system that can generate attractive playlist covers from a playlist URL. Users will be able to input a playlist link and receive a custom-generated cover that captures the musical vibe and aesthetic.

## Current Phase: Color Extraction

Starting simple:
- Upload a set of images
- Extract n representative RGB colors that preserve the "vibe" of the images
- Display the extracted color palette

This foundation will later be expanded to include:
- Playlist URL parsing
- Music metadata analysis
- Automatic cover generation
- Style customization options

## Architecture

**Backend**: Python for image processing and color extraction
**Frontend**: Simple web UI for image uploads and color display
**Core Algorithm**: K-means clustering for dominant color extraction

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Upload images and specify number of colors to extract
4. View your extracted color palette

## Future Enhancements

- Playlist integration (Spotify, Apple Music, etc.)
- Advanced color harmony algorithms
- Multiple cover design templates
- Batch processing capabilities
- API for programmatic access