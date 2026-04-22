/**
 * Utility to extract chart images from canvas/DOM elements
 * Converts chart visualizations to PNG for PDF embedding
 * 
 * Usage:
 * const imageData = extractCanvasImage('my-chart-canvas');
 * pdf.addImage(imageData, 'PNG', x, y, width, height);
 */

export interface ChartImage {
  data: string;  // base64 PNG data
  width: number; // width in mm for PDF
  height: number; // height in mm for PDF
  title: string;
}

/**
 * Extract image from canvas element
 * Works with Chart.js, Recharts canvas exports, or any canvas element
 * 
 * @param canvasId - ID of canvas element
 * @returns Base64 PNG image data or null if failed
 */
export function extractCanvasImage(canvasId: string): string | null {
  const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
  if (!canvas) {
    console.warn(`Canvas element with id "${canvasId}" not found`);
    return null;
  }
  try {
    return canvas.toDataURL('image/png');
  } catch (err) {
    console.error(`Failed to extract image from canvas ${canvasId}:`, err);
    return null;
  }
}

/**
 * Extract image from SVG element
 * Converts SVG to PNG for PDF compatibility
 * 
 * @param svgId - ID of SVG element
 * @returns Promise with base64 PNG data or null if failed
 */
export async function extractSVGImage(svgId: string): Promise<string | null> {
  const svgElement = document.getElementById(svgId) as SVGElement;
  if (!svgElement) {
    console.warn(`SVG element with id "${svgId}" not found`);
    return null;
  }

  try {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    const svg = new XMLSerializer().serializeToString(svgElement);
    const img = new Image();
    img.crossOrigin = 'anonymous';

    return new Promise((resolve) => {
      img.onload = () => {
        canvas.width = img.width || 400;
        canvas.height = img.height || 300;
        ctx.drawImage(img, 0, 0);
        resolve(canvas.toDataURL('image/png'));
      };
      img.onerror = () => {
        console.error(`Failed to load SVG image: ${svgId}`);
        resolve(null);
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(svg);
    });
  } catch (err) {
    console.error(`Failed to extract image from SVG ${svgId}:`, err);
    return null;
  }
}

/**
 * Create placeholder chart image for testing/fallback
 * Useful when actual chart data is not available
 * 
 * @param title - Title to display on placeholder
 * @param width - Canvas width in pixels
 * @param height - Canvas height in pixels
 * @returns Base64 PNG image data
 */
export function createPlaceholderChartImage(
  title: string,
  width: number = 400,
  height: number = 300
): string {
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');

  if (!ctx) return '';

  // Draw dark background
  ctx.fillStyle = '#1e293b';
  ctx.fillRect(0, 0, width, height);

  // Draw border
  ctx.strokeStyle = '#3b82f6';
  ctx.lineWidth = 2;
  ctx.strokeRect(5, 5, width - 10, height - 10);

  // Draw placeholder text
  ctx.fillStyle = '#94a3b8';
  ctx.font = 'bold 16px Arial';
  ctx.textAlign = 'center';
  ctx.fillText(title, width / 2, height / 2 - 20);
  ctx.font = '12px Arial';
  ctx.fillText('(Chart data will be populated)', width / 2, height / 2 + 10);

  return canvas.toDataURL('image/png');
}

/**
 * Batch extract multiple chart images
 * Handles multiple chart IDs and returns array of ChartImage objects
 * 
 * @param chartIds - Array of canvas/SVG element IDs
 * @returns Array of ChartImage objects (failed extractions are filtered out)
 */
export function extractMultipleCharts(chartIds: string[]): ChartImage[] {
  return chartIds
    .map(id => {
      const imageData = extractCanvasImage(id);
      if (!imageData) return null;

      return {
        data: imageData,
        width: 160, // mm for PDF
        height: 120,
        title: id.replace(/-/g, ' ').toUpperCase()
      };
    })
    .filter((img) => img !== null) as ChartImage[];
}

/**
 * Extract and scale image to fit PDF page
 * Automatically calculates dimensions to fit within margins
 * 
 * @param canvasId - Canvas element ID
 * @param maxWidth - Maximum width in mm (default 160)
 * @param maxHeight - Maximum height in mm (default 120)
 * @returns ChartImage object with scaled dimensions
 */
export function extractAndScaleChart(
  canvasId: string,
  maxWidth: number = 160,
  maxHeight: number = 120
): ChartImage | null {
  const imageData = extractCanvasImage(canvasId);
  if (!imageData) return null;

  // Get canvas aspect ratio
  const canvas = document.getElementById(canvasId) as HTMLCanvasElement;
  if (!canvas) return null;

  const aspectRatio = canvas.width / canvas.height;
  let width = maxWidth;
  let height = width / aspectRatio;

  if (height > maxHeight) {
    height = maxHeight;
    width = height * aspectRatio;
  }

  return {
    data: imageData,
    width,
    height,
    title: canvasId.replace(/-/g, ' ').toUpperCase()
  };
}

/**
 * Append image data URI to PDF (helper for React component)
 * Usage in ReportExporter.tsx:
 * const img = extractCanvasImage('roc-chart');
 * pdf.addImage(img, 'PNG', 15, yPosition, 160, 120);
 */
export const chartExtractorUtils = {
  extractCanvasImage,
  extractSVGImage,
  createPlaceholderChartImage,
  extractMultipleCharts,
  extractAndScaleChart
};

export default chartExtractorUtils;
