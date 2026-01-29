/**
 * Canvas-based board renderer with enhanced visuals and animations
 */

import { useRef, useEffect, useCallback, useState } from 'react';
import type { Piece, Position } from '../../types/game';
import {
  BOARD_ROWS,
  BOARD_COLS,
  CELL_SIZE,
  BOARD_PADDING,
  PIECE_RADIUS,
  CANVAS_WIDTH,
  CANVAS_HEIGHT,
  COLORS,
  PIECE_NAMES,
  posToCanvas,
  canvasToPos,
} from './constants';

interface BoardCanvasProps {
  board: (Piece | null)[][] | null;
  selectedPiece: Position | null;
  legalMoves: Position[];
  lastMove: { from: [number, number]; to: [number, number] } | null;
  isCheck: boolean;
  currentTurn: 'red' | 'black';
  playerColor: 'red' | 'black';
  onCellClick: (row: number, col: number) => void;
}

// Animation state
interface AnimationState {
  piece: Piece;
  fromX: number;
  fromY: number;
  toX: number;
  toY: number;
  progress: number;
  fromRow: number;
  fromCol: number;
  toRow: number;
  toCol: number;
}

export function BoardCanvas({
  board,
  selectedPiece,
  legalMoves,
  lastMove,
  isCheck,
  currentTurn,
  playerColor,
  onCellClick,
}: BoardCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [animation, setAnimation] = useState<AnimationState | null>(null);
  const animationRef = useRef<number | null>(null);
  const prevLastMoveRef = useRef<{ from: [number, number]; to: [number, number] } | null>(null);

  // Detect new move and start animation
  useEffect(() => {
    if (lastMove && board) {
      const prevMove = prevLastMoveRef.current;
      const isNewMove = !prevMove ||
        prevMove.from[0] !== lastMove.from[0] ||
        prevMove.from[1] !== lastMove.from[1] ||
        prevMove.to[0] !== lastMove.to[0] ||
        prevMove.to[1] !== lastMove.to[1];

      if (isNewMove) {
        const piece = board[lastMove.to[0]]?.[lastMove.to[1]];
        if (piece) {
          const from = posToCanvas(lastMove.from[0], lastMove.from[1]);
          const to = posToCanvas(lastMove.to[0], lastMove.to[1]);

          setAnimation({
            piece,
            fromX: from.x,
            fromY: from.y,
            toX: to.x,
            toY: to.y,
            progress: 0,
            fromRow: lastMove.from[0],
            fromCol: lastMove.from[1],
            toRow: lastMove.to[0],
            toCol: lastMove.to[1],
          });
        }
      }
      prevLastMoveRef.current = lastMove;
    }
  }, [lastMove, board]);

  // Animation loop
  useEffect(() => {
    if (!animation) return;

    const animate = () => {
      setAnimation(prev => {
        if (!prev) return null;
        const newProgress = prev.progress + 0.08; // Animation speed
        if (newProgress >= 1) {
          return null; // Animation complete
        }
        return { ...prev, progress: newProgress };
      });
      animationRef.current = requestAnimationFrame(animate);
    };

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [animation?.piece]);

  // Draw wood texture pattern
  const drawWoodTexture = useCallback((ctx: CanvasRenderingContext2D) => {
    // Create wood grain gradient
    const gradient = ctx.createLinearGradient(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    gradient.addColorStop(0, '#DEB887');
    gradient.addColorStop(0.3, '#D2A679');
    gradient.addColorStop(0.5, '#C4956A');
    gradient.addColorStop(0.7, '#D2A679');
    gradient.addColorStop(1, '#DEB887');

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // Add subtle wood grain lines
    ctx.strokeStyle = 'rgba(139, 90, 43, 0.15)';
    ctx.lineWidth = 1;

    for (let i = 0; i < 30; i++) {
      const y = (i * CANVAS_HEIGHT / 30) + Math.sin(i * 0.5) * 5;
      ctx.beginPath();
      ctx.moveTo(0, y);

      // Wavy line for wood grain effect
      for (let x = 0; x < CANVAS_WIDTH; x += 20) {
        const waveY = y + Math.sin(x * 0.02 + i) * 3;
        ctx.lineTo(x, waveY);
      }
      ctx.stroke();
    }

    // Add some darker spots for wood knots
    ctx.fillStyle = 'rgba(101, 67, 33, 0.08)';
    const knotPositions = [
      [80, 120], [400, 300], [200, 500], [450, 150], [100, 400]
    ];
    knotPositions.forEach(([kx, ky]) => {
      ctx.beginPath();
      ctx.ellipse(kx, ky, 15, 10, Math.random() * Math.PI, 0, Math.PI * 2);
      ctx.fill();
    });
  }, []);

  const drawBoard = useCallback((ctx: CanvasRenderingContext2D) => {
    // Draw wood texture background
    drawWoodTexture(ctx);

    // Draw board border with shadow effect
    ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
    ctx.shadowBlur = 10;
    ctx.shadowOffsetX = 3;
    ctx.shadowOffsetY = 3;

    ctx.strokeStyle = '#5D3A1A';
    ctx.lineWidth = 4;
    ctx.strokeRect(BOARD_PADDING - 15, BOARD_PADDING - 15,
      CANVAS_WIDTH - BOARD_PADDING * 2 + 30,
      CANVAS_HEIGHT - BOARD_PADDING * 2 + 30);

    // Reset shadow
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    // Draw grid lines with enhanced style
    ctx.strokeStyle = '#4A3728';
    ctx.lineWidth = 1.5;

    // Draw horizontal lines
    for (let row = 0; row < BOARD_ROWS; row++) {
      const { x: x1, y } = posToCanvas(row, 0);
      const { x: x2 } = posToCanvas(row, BOARD_COLS - 1);
      ctx.beginPath();
      ctx.moveTo(x1, y);
      ctx.lineTo(x2, y);
      ctx.stroke();
    }

    // Draw vertical lines (with river gap)
    for (let col = 0; col < BOARD_COLS; col++) {
      const { x, y: y1 } = posToCanvas(0, col);
      const { y: y2 } = posToCanvas(4, col);
      ctx.beginPath();
      ctx.moveTo(x, y1);
      ctx.lineTo(x, y2);
      ctx.stroke();

      const { y: y3 } = posToCanvas(5, col);
      const { y: y4 } = posToCanvas(9, col);
      ctx.beginPath();
      ctx.moveTo(x, y3);
      ctx.lineTo(x, y4);
      ctx.stroke();

      if (col === 0 || col === BOARD_COLS - 1) {
        ctx.beginPath();
        ctx.moveTo(x, y2);
        ctx.lineTo(x, y3);
        ctx.stroke();
      }
    }

    // Draw palace diagonals
    ctx.strokeStyle = '#4A3728';
    ctx.lineWidth = 1.5;

    // Top palace
    let p1 = posToCanvas(0, 3);
    let p2 = posToCanvas(2, 5);
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    p1 = posToCanvas(0, 5);
    p2 = posToCanvas(2, 3);
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    // Bottom palace
    p1 = posToCanvas(7, 3);
    p2 = posToCanvas(9, 5);
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    p1 = posToCanvas(7, 5);
    p2 = posToCanvas(9, 3);
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();

    // Draw cannon/pawn position markers
    const markerPositions = [
      // Cannon positions
      [2, 1], [2, 7], [7, 1], [7, 7],
      // Pawn positions
      [3, 0], [3, 2], [3, 4], [3, 6], [3, 8],
      [6, 0], [6, 2], [6, 4], [6, 6], [6, 8],
    ];

    ctx.strokeStyle = '#4A3728';
    ctx.lineWidth = 1.5;
    const markerSize = 6;
    const markerGap = 3;

    markerPositions.forEach(([row, col]) => {
      const { x, y } = posToCanvas(row, col);

      // Draw L-shaped markers at corners
      const corners = [
        { dx: -1, dy: -1, skipLeft: col === 0, skipRight: false },
        { dx: 1, dy: -1, skipLeft: false, skipRight: col === 8 },
        { dx: -1, dy: 1, skipLeft: col === 0, skipRight: false },
        { dx: 1, dy: 1, skipLeft: false, skipRight: col === 8 },
      ];

      corners.forEach(({ dx, dy, skipLeft, skipRight }) => {
        if ((dx < 0 && skipLeft) || (dx > 0 && skipRight)) return;

        ctx.beginPath();
        ctx.moveTo(x + dx * markerGap, y + dy * (markerGap + markerSize));
        ctx.lineTo(x + dx * markerGap, y + dy * markerGap);
        ctx.lineTo(x + dx * (markerGap + markerSize), y + dy * markerGap);
        ctx.stroke();
      });
    });

    // Draw river with enhanced style
    const riverY1 = posToCanvas(4, 0).y;
    const riverY2 = posToCanvas(5, 0).y;
    const riverGradient = ctx.createLinearGradient(0, riverY1, 0, riverY2);
    riverGradient.addColorStop(0, 'rgba(176, 196, 222, 0.2)');
    riverGradient.addColorStop(0.5, 'rgba(176, 196, 222, 0.35)');
    riverGradient.addColorStop(1, 'rgba(176, 196, 222, 0.2)');

    ctx.fillStyle = riverGradient;
    ctx.fillRect(BOARD_PADDING, riverY1, CANVAS_WIDTH - BOARD_PADDING * 2, riverY2 - riverY1);

    // Draw river text with shadow
    ctx.shadowColor = 'rgba(255, 255, 255, 0.8)';
    ctx.shadowBlur = 2;
    ctx.fillStyle = '#5D3A1A';
    ctx.font = 'bold 22px "KaiTi", "STKaiti", serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    const riverY = (riverY1 + riverY2) / 2;
    ctx.fillText('楚  河', posToCanvas(0, 2).x, riverY);
    ctx.fillText('漢  界', posToCanvas(0, 6).x, riverY);

    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
  }, [drawWoodTexture]);

  const drawLastMoveHighlight = useCallback((ctx: CanvasRenderingContext2D) => {
    if (!lastMove) return;

    const fromPos = posToCanvas(lastMove.from[0], lastMove.from[1]);
    const toPos = posToCanvas(lastMove.to[0], lastMove.to[1]);

    // Draw "from" position marker (where the piece was)
    ctx.strokeStyle = '#FF6B6B';
    ctx.lineWidth = 3;
    ctx.setLineDash([5, 3]);

    // Draw corner brackets for "from" position
    const bracketSize = 12;
    const bracketOffset = PIECE_RADIUS + 6;

    // From position - dashed square corners
    const drawCornerBrackets = (x: number, y: number, color: string, dashed: boolean) => {
      ctx.strokeStyle = color;
      ctx.lineWidth = 3;
      ctx.setLineDash(dashed ? [5, 3] : []);

      // Top-left
      ctx.beginPath();
      ctx.moveTo(x - bracketOffset, y - bracketOffset + bracketSize);
      ctx.lineTo(x - bracketOffset, y - bracketOffset);
      ctx.lineTo(x - bracketOffset + bracketSize, y - bracketOffset);
      ctx.stroke();

      // Top-right
      ctx.beginPath();
      ctx.moveTo(x + bracketOffset - bracketSize, y - bracketOffset);
      ctx.lineTo(x + bracketOffset, y - bracketOffset);
      ctx.lineTo(x + bracketOffset, y - bracketOffset + bracketSize);
      ctx.stroke();

      // Bottom-left
      ctx.beginPath();
      ctx.moveTo(x - bracketOffset, y + bracketOffset - bracketSize);
      ctx.lineTo(x - bracketOffset, y + bracketOffset);
      ctx.lineTo(x - bracketOffset + bracketSize, y + bracketOffset);
      ctx.stroke();

      // Bottom-right
      ctx.beginPath();
      ctx.moveTo(x + bracketOffset - bracketSize, y + bracketOffset);
      ctx.lineTo(x + bracketOffset, y + bracketOffset);
      ctx.lineTo(x + bracketOffset, y + bracketOffset - bracketSize);
      ctx.stroke();
    };

    // Draw from position (dashed, lighter color)
    drawCornerBrackets(fromPos.x, fromPos.y, 'rgba(255, 107, 107, 0.7)', true);

    // Draw to position (solid, brighter color)
    drawCornerBrackets(toPos.x, toPos.y, '#FF4757', false);

    ctx.setLineDash([]);
  }, [lastMove]);

  const drawHighlights = useCallback((ctx: CanvasRenderingContext2D) => {
    // Draw last move highlight first
    drawLastMoveHighlight(ctx);

    // Draw selected piece highlight
    if (selectedPiece) {
      const pos = posToCanvas(selectedPiece.row, selectedPiece.col);

      // Glowing effect
      const gradient = ctx.createRadialGradient(pos.x, pos.y, PIECE_RADIUS - 5, pos.x, pos.y, PIECE_RADIUS + 10);
      gradient.addColorStop(0, 'rgba(255, 215, 0, 0.6)');
      gradient.addColorStop(0.7, 'rgba(255, 215, 0, 0.3)');
      gradient.addColorStop(1, 'rgba(255, 215, 0, 0)');

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(pos.x, pos.y, PIECE_RADIUS + 10, 0, Math.PI * 2);
      ctx.fill();
    }

    // Draw legal move indicators
    for (const move of legalMoves) {
      const pos = posToCanvas(move.row, move.col);
      const piece = board?.[move.row]?.[move.col];

      if (piece) {
        // Capture indicator - pulsing ring
        ctx.strokeStyle = '#E74C3C';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, PIECE_RADIUS + 5, 0, Math.PI * 2);
        ctx.stroke();

        // Inner glow
        ctx.strokeStyle = 'rgba(231, 76, 60, 0.5)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, PIECE_RADIUS + 8, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        // Empty square indicator - gradient dot
        const dotGradient = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, 10);
        dotGradient.addColorStop(0, '#2ECC71');
        dotGradient.addColorStop(0.6, 'rgba(46, 204, 113, 0.8)');
        dotGradient.addColorStop(1, 'rgba(46, 204, 113, 0.3)');

        ctx.fillStyle = dotGradient;
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, 10, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }, [selectedPiece, legalMoves, board, drawLastMoveHighlight]);

  const drawPiece = useCallback((
    ctx: CanvasRenderingContext2D,
    piece: Piece,
    x: number,
    y: number,
    isInCheck: boolean,
    isAnimating: boolean = false
  ) => {
    const isRed = piece.color === 'red';

    // Shadow for 3D effect
    if (!isAnimating) {
      ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
      ctx.shadowBlur = 6;
      ctx.shadowOffsetX = 3;
      ctx.shadowOffsetY = 3;
    } else {
      // Larger shadow for animating piece (lifted effect)
      ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
      ctx.shadowBlur = 12;
      ctx.shadowOffsetX = 6;
      ctx.shadowOffsetY = 6;
    }

    // Outer ring (wood-like border)
    ctx.beginPath();
    ctx.arc(x, y, PIECE_RADIUS, 0, Math.PI * 2);
    const outerGradient = ctx.createRadialGradient(x - 5, y - 5, 0, x, y, PIECE_RADIUS);
    outerGradient.addColorStop(0, '#8B7355');
    outerGradient.addColorStop(0.7, '#6B5344');
    outerGradient.addColorStop(1, '#4A3728');
    ctx.fillStyle = outerGradient;
    ctx.fill();

    // Reset shadow for inner parts
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;

    // Check highlight
    if (isInCheck && piece.type === 'K') {
      ctx.strokeStyle = '#FF0000';
      ctx.lineWidth = 4;
      ctx.stroke();

      // Pulsing glow effect
      ctx.shadowColor = 'rgba(255, 0, 0, 0.6)';
      ctx.shadowBlur = 15;
    }

    // Inner piece face with gradient (ivory/cream color)
    ctx.beginPath();
    ctx.arc(x, y, PIECE_RADIUS - 3, 0, Math.PI * 2);
    const innerGradient = ctx.createRadialGradient(x - 8, y - 8, 0, x, y, PIECE_RADIUS - 3);
    if (isRed) {
      innerGradient.addColorStop(0, '#FFFEF5');
      innerGradient.addColorStop(0.5, '#FFF8E7');
      innerGradient.addColorStop(1, '#F5E6D3');
    } else {
      innerGradient.addColorStop(0, '#FFFEF5');
      innerGradient.addColorStop(0.5, '#FFF8E7');
      innerGradient.addColorStop(1, '#F0E4D4');
    }
    ctx.fillStyle = innerGradient;
    ctx.fill();

    // Inner decorative ring
    ctx.beginPath();
    ctx.arc(x, y, PIECE_RADIUS - 6, 0, Math.PI * 2);
    ctx.strokeStyle = isRed ? '#8B0000' : '#1A1A1A';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Second inner ring for traditional look
    ctx.beginPath();
    ctx.arc(x, y, PIECE_RADIUS - 9, 0, Math.PI * 2);
    ctx.strokeStyle = isRed ? 'rgba(139, 0, 0, 0.5)' : 'rgba(26, 26, 26, 0.5)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Reset shadow
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;

    // Piece text with enhanced styling
    ctx.fillStyle = isRed ? '#8B0000' : '#1A1A1A';
    ctx.font = 'bold 26px "KaiTi", "STKaiti", "SimSun", serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // Text shadow for depth
    ctx.shadowColor = isRed ? 'rgba(139, 0, 0, 0.3)' : 'rgba(0, 0, 0, 0.3)';
    ctx.shadowBlur = 1;
    ctx.shadowOffsetX = 1;
    ctx.shadowOffsetY = 1;

    const name = PIECE_NAMES[piece.color][piece.type];
    ctx.fillText(name, x, y + 1);

    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
  }, []);

  const drawPieces = useCallback((ctx: CanvasRenderingContext2D) => {
    if (!board) return;

    for (let row = 0; row < BOARD_ROWS; row++) {
      for (let col = 0; col < BOARD_COLS; col++) {
        // Skip the animating piece at its destination during animation
        if (animation && animation.toRow === row && animation.toCol === col) {
          continue;
        }

        const piece = board[row]?.[col];
        if (piece) {
          const { x, y } = posToCanvas(row, col);
          const isKingInCheck = isCheck && piece.type === 'K' && piece.color === currentTurn;
          drawPiece(ctx, piece, x, y, isKingInCheck);
        }
      }
    }

    // Draw animating piece on top
    if (animation) {
      const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);
      const easedProgress = easeOutCubic(animation.progress);

      const currentX = animation.fromX + (animation.toX - animation.fromX) * easedProgress;
      const currentY = animation.fromY + (animation.toY - animation.fromY) * easedProgress;

      const isKingInCheck = isCheck && animation.piece.type === 'K' && animation.piece.color === currentTurn;
      drawPiece(ctx, animation.piece, currentX, currentY, isKingInCheck, true);
    }
  }, [board, isCheck, currentTurn, drawPiece, animation]);

  const render = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    drawBoard(ctx);
    drawHighlights(ctx);
    drawPieces(ctx);
  }, [drawBoard, drawHighlights, drawPieces]);

  useEffect(() => {
    render();
  }, [render]);

  const handleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    // Ignore clicks during animation
    if (animation) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;

    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    const pos = canvasToPos(x, y);
    if (pos) {
      onCellClick(pos.row, pos.col);
    }
  }, [onCellClick, animation]);

  return (
    <canvas
      ref={canvasRef}
      width={CANVAS_WIDTH}
      height={CANVAS_HEIGHT}
      onClick={handleClick}
      className="cursor-pointer max-w-full h-auto rounded-lg shadow-2xl"
      style={{
        maxHeight: '80vh',
        border: '8px solid #5D3A1A',
        borderRadius: '12px',
        boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(0, 0, 0, 0.1)'
      }}
    />
  );
}
