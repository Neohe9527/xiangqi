/**
 * Board constants and configuration
 */

// Board dimensions
export const BOARD_ROWS = 10;
export const BOARD_COLS = 9;

// Canvas sizing
export const CELL_SIZE = 60;
export const BOARD_PADDING = 40;
export const PIECE_RADIUS = 26;

export const CANVAS_WIDTH = CELL_SIZE * (BOARD_COLS - 1) + BOARD_PADDING * 2;
export const CANVAS_HEIGHT = CELL_SIZE * (BOARD_ROWS - 1) + BOARD_PADDING * 2;

// Colors
export const COLORS = {
  boardBg: '#EBC88C',
  boardLine: '#654321',
  river: '#B0C4DE',
  selected: '#FFD700',
  legalMove: '#2ECC71',
  lastMove: '#87CEEB',
  check: '#E74C3C',
  pieceRed: '#C0392B',
  pieceBlack: '#2C3E50',
  pieceBgRed: '#FFFAF0',
  pieceBgBlack: '#F5F5DC',
  pieceBorderRed: '#8B0000',
  pieceBorderBlack: '#191919',
};

// Piece Chinese names
export const PIECE_NAMES: Record<string, Record<string, string>> = {
  red: {
    K: '帅',
    A: '仕',
    E: '相',
    H: '马',
    R: '车',
    C: '炮',
    P: '兵',
  },
  black: {
    K: '将',
    A: '士',
    E: '象',
    H: '马',
    R: '车',
    C: '炮',
    P: '卒',
  },
};

// Convert board position to canvas coordinates
export function posToCanvas(row: number, col: number): { x: number; y: number } {
  return {
    x: BOARD_PADDING + col * CELL_SIZE,
    y: BOARD_PADDING + row * CELL_SIZE,
  };
}

// Convert canvas coordinates to board position
export function canvasToPos(x: number, y: number): { row: number; col: number } | null {
  const col = Math.round((x - BOARD_PADDING) / CELL_SIZE);
  const row = Math.round((y - BOARD_PADDING) / CELL_SIZE);

  if (row >= 0 && row < BOARD_ROWS && col >= 0 && col < BOARD_COLS) {
    // Check if click is close enough to intersection
    const { x: targetX, y: targetY } = posToCanvas(row, col);
    const distance = Math.sqrt((x - targetX) ** 2 + (y - targetY) ** 2);
    if (distance <= CELL_SIZE / 2) {
      return { row, col };
    }
  }

  return null;
}
