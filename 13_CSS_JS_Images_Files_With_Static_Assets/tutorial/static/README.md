# Static Assets Directory

This directory contains static assets served by the Pyramid application:

## Files:
- `app.css` - Main stylesheet with modern CSS features
- `app.js` - Interactive JavaScript functionality
- `logo.png` - Logo image (placeholder - replace with actual PNG)

## Features Demonstrated:
- CSS Grid and Flexbox layouts
- CSS animations and transitions
- Responsive design with media queries
- JavaScript DOM manipulation
- Event handling
- Performance monitoring
- Dynamic content updates

## Static URL Generation:
In templates, static assets are referenced using:
```
{{ request.static_url('tutorial:static/filename.ext') }}
```

This generates proper URLs that work in both development and production environments.
