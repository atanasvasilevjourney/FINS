import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { PuzzleGenerator } from '../services/PuzzleGenerator';
import { BulgarianDictionary } from '../services/BulgarianDictionary';
import { PointsCalculator } from '../utils/PointsCalculator';

// Async thunks
export const loadPuzzle = createAsyncThunk(
  'game/loadPuzzle',
  async ({ difficulty, theme }) => {
    const puzzle = await PuzzleGenerator.generatePuzzle(difficulty, theme);
    return puzzle;
  }
);

export const submitWord = createAsyncThunk(
  'game/submitWord',
  async ({ word, positions, clueId }, { getState }) => {
    const { game } = getState();
    const isCorrect = BulgarianDictionary.validateWord(word);
    
    if (isCorrect) {
      const points = PointsCalculator.calculateWordPoints(
        word, 
        game.currentTime, 
        game.hintsUsed, 
        game.difficulty
      );
      
      return { word, positions, clueId, points };
    } else {
      throw new Error('Невалидна дума');
    }
  }
);

const gameSlice = createSlice({
  name: 'game',
  initialState: {
    currentPuzzle: null,
    selectedCells: [],
    currentWord: '',
    score: 0,
    level: 1,
    difficulty: 1,
    theme: 'nature',
    hintsUsed: 0,
    hintsAvailable: 3,
    gameState: 'idle', // idle, playing, paused, completed
    startTime: null,
    currentTime: 0,
    loading: false,
    error: null,
    currentHint: null
  },
  reducers: {
    selectCell: (state, action) => {
      const { row, col } = action.payload;
      const cellKey = `${row}-${col}`;
      
      if (state.selectedCells.includes(cellKey)) {
        state.selectedCells = state.selectedCells.filter(cell => cell !== cellKey);
      } else {
        state.selectedCells.push(cellKey);
      }
      
      // Update current word
      state.currentWord = buildWordFromCells(state.selectedCells, state.currentPuzzle);
    },
    
    clearSelection: (state) => {
      state.selectedCells = [];
      state.currentWord = '';
      state.currentHint = null;
    },
    
    useHint: (state, action) => {
      if (state.hintsAvailable > 0) {
        state.hintsAvailable--;
        state.hintsUsed++;
        
        const hint = generateHint(state.currentPuzzle, action.payload.clueId);
        state.currentHint = hint;
      }
    },
    
    updateTimer: (state) => {
      if (state.gameState === 'playing' && state.startTime) {
        state.currentTime = Date.now() - state.startTime;
      }
    },
    
    pauseGame: (state) => {
      state.gameState = 'paused';
    },
    
    resumeGame: (state) => {
      state.gameState = 'playing';
    },
    
    resetGame: (state) => {
      state.currentPuzzle = null;
      state.selectedCells = [];
      state.currentWord = '';
      state.score = 0;
      state.hintsUsed = 0;
      state.hintsAvailable = 3;
      state.gameState = 'idle';
      state.startTime = null;
      state.currentTime = 0;
      state.error = null;
      state.currentHint = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadPuzzle.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadPuzzle.fulfilled, (state, action) => {
        state.loading = false;
        state.currentPuzzle = action.payload;
        state.gameState = 'playing';
        state.startTime = Date.now();
        state.hintsAvailable = 3;
        state.hintsUsed = 0;
      })
      .addCase(loadPuzzle.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(submitWord.fulfilled, (state, action) => {
        const { word, positions, clueId, points } = action.payload;
        
        // Mark word as solved
        const clue = state.currentPuzzle.clues.find(c => c.id === clueId);
        if (clue) {
          clue.solved = true;
        }
        
        // Update score
        state.score += points;
        
        // Clear selection
        state.selectedCells = [];
        state.currentWord = '';
        state.currentHint = null;
        
        // Check if puzzle is completed
        const allSolved = state.currentPuzzle.clues.every(c => c.solved);
        if (allSolved) {
          state.gameState = 'completed';
        }
      })
      .addCase(submitWord.rejected, (state, action) => {
        state.error = action.error.message;
      });
  }
});

// Helper functions
const buildWordFromCells = (selectedCells, puzzle) => {
  if (!puzzle || selectedCells.length === 0) return '';
  
  const sortedCells = selectedCells
    .map(cell => {
      const [row, col] = cell.split('-').map(Number);
      return { row, col };
    })
    .sort((a, b) => {
      if (a.row !== b.row) return a.row - b.row;
      return a.col - b.col;
    });
  
  return sortedCells
    .map(cell => puzzle.letters[cell.row][cell.col].letter)
    .join('');
};

const generateHint = (puzzle, clueId) => {
  const clue = puzzle.clues.find(c => c.id === clueId);
  if (!clue) return null;
  
  const word = clue.text;
  const hintLength = Math.ceil(word.length * 0.3); // Show 30% of letters
  
  let hint = '';
  for (let i = 0; i < word.length; i++) {
    if (i < hintLength || Math.random() < 0.1) {
      hint += word[i];
    } else {
      hint += '_';
    }
  }
  
  return hint;
};

export const { 
  selectCell, 
  clearSelection, 
  useHint, 
  updateTimer, 
  pauseGame, 
  resumeGame,
  resetGame
} = gameSlice.actions;

export default gameSlice.reducer; 