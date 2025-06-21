import { PUZZLE_THEMES } from '../data/puzzleThemes';
import { BulgarianDictionary } from './BulgarianDictionary';

export class PuzzleGenerator {
  static async generatePuzzle(difficulty = 1, theme = 'nature') {
    const themeData = PUZZLE_THEMES[theme] || PUZZLE_THEMES.nature;
    const config = this.getDifficultyConfig(difficulty);
    
    // Select words for this puzzle
    const selectedWords = this.selectWordsForPuzzle(themeData.words, config.wordCount, config.maxWordLength);
    
    // Generate crossword grid
    const grid = this.generateCrosswordGrid(selectedWords, config.gridSize);
    
    // Create clues
    const clues = this.createClues(selectedWords, themeData.clues);
    
    return {
      id: `puzzle_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      theme,
      difficulty,
      size: { rows: config.gridSize, cols: config.gridSize },
      letters: grid,
      words: selectedWords,
      clues,
      createdAt: new Date().toISOString(),
      estimatedTime: config.estimatedTime,
      maxPoints: this.calculateMaxPoints(selectedWords, difficulty)
    };
  }
  
  static getDifficultyConfig(difficulty) {
    const configs = {
      1: { gridSize: 7, wordCount: 5, maxWordLength: 6, estimatedTime: 300 },
      2: { gridSize: 9, wordCount: 7, maxWordLength: 8, estimatedTime: 450 },
      3: { gridSize: 11, wordCount: 9, maxWordLength: 10, estimatedTime: 600 },
      4: { gridSize: 13, wordCount: 12, maxWordLength: 12, estimatedTime: 900 },
      5: { gridSize: 15, wordCount: 15, maxWordLength: 15, estimatedTime: 1200 }
    };
    
    return configs[difficulty] || configs[1];
  }
  
  static selectWordsForPuzzle(themeWords, wordCount, maxLength) {
    const availableWords = themeWords.filter(word => word.length <= maxLength);
    const shuffled = this.shuffleArray([...availableWords]);
    
    return shuffled.slice(0, wordCount).map((word, index) => ({
      id: `word_${index + 1}`,
      text: word,
      length: word.length,
      solved: false,
      direction: index % 2 === 0 ? 'horizontal' : 'vertical'
    }));
  }
  
  static generateCrosswordGrid(words, gridSize) {
    const grid = Array(gridSize).fill(null).map(() => 
      Array(gridSize).fill(null).map(() => ({ letter: '', used: false, position: [0, 0] }))
    );
    
    let placedWords = [];
    
    words.forEach((word, wordIndex) => {
      const placed = this.placeWordInGrid(grid, word, placedWords, wordIndex);
      if (placed) {
        placedWords.push(placed);
      }
    });
    
    // Fill empty cells with random Bulgarian letters
    this.fillEmptyCells(grid);
    
    return grid;
  }
  
  static placeWordInGrid(grid, word, placedWords, wordIndex) {
    const maxAttempts = 100;
    let attempts = 0;
    
    while (attempts < maxAttempts) {
      const direction = word.direction;
      const wordLength = word.text.length;
      
      // Try to find a valid position
      const position = this.findValidPosition(grid, wordLength, direction, placedWords);
      
      if (position) {
        const { row, col } = position;
        
        // Place the word
        for (let i = 0; i < wordLength; i++) {
          const currentRow = direction === 'horizontal' ? row : row + i;
          const currentCol = direction === 'horizontal' ? col + i : col;
          
          if (currentRow < grid.length && currentCol < grid[0].length) {
            grid[currentRow][currentCol] = {
              letter: word.text[i],
              used: true,
              position: [currentRow, currentCol],
              wordIds: [word.id]
            };
          }
        }
        
        return {
          word,
          position,
          direction
        };
      }
      
      attempts++;
    }
    
    return null;
  }
  
  static findValidPosition(grid, wordLength, direction, placedWords) {
    const gridSize = grid.length;
    const maxRow = direction === 'horizontal' ? gridSize : gridSize - wordLength;
    const maxCol = direction === 'horizontal' ? gridSize - wordLength : gridSize;
    
    for (let row = 0; row < maxRow; row++) {
      for (let col = 0; col < maxCol; col++) {
        if (this.canPlaceWord(grid, row, col, wordLength, direction)) {
          return { row, col };
        }
      }
    }
    
    return null;
  }
  
  static canPlaceWord(grid, row, col, wordLength, direction) {
    for (let i = 0; i < wordLength; i++) {
      const currentRow = direction === 'horizontal' ? row : row + i;
      const currentCol = direction === 'horizontal' ? col + i : col;
      
      if (currentRow >= grid.length || currentCol >= grid[0].length) {
        return false;
      }
      
      const cell = grid[currentRow][currentCol];
      if (cell.letter !== '' && cell.letter !== '') {
        return false;
      }
    }
    
    return true;
  }
  
  static fillEmptyCells(grid) {
    const bulgarianLetters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЬЮЯ';
    
    for (let row = 0; row < grid.length; row++) {
      for (let col = 0; col < grid[0].length; col++) {
        if (grid[row][col].letter === '') {
          const randomLetter = bulgarianLetters[Math.floor(Math.random() * bulgarianLetters.length)];
          grid[row][col] = {
            letter: randomLetter,
            used: false,
            position: [row, col],
            wordIds: []
          };
        }
      }
    }
  }
  
  static createClues(words, themeClues) {
    return words.map(word => ({
      id: word.id,
      word: word.text,
      clue: themeClues[word.text] || `Дума с ${word.length} букви`,
      direction: word.direction,
      solved: false
    }));
  }
  
  static calculateMaxPoints(words, difficulty) {
    const basePoints = words.reduce((total, word) => total + word.length * 10, 0);
    const difficultyMultiplier = { 1: 1.0, 2: 1.2, 3: 1.5, 4: 1.8, 5: 2.0 };
    return Math.floor(basePoints * difficultyMultiplier[difficulty]);
  }
  
  static shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }
  
  static generateDailyChallenge() {
    const today = new Date().toISOString().split('T')[0];
    const seed = this.hashString(today);
    
    // Use seed to ensure consistent daily puzzle
    const themes = Object.keys(PUZZLE_THEMES);
    const theme = themes[seed % themes.length];
    
    return this.generatePuzzle(2, theme); // Medium difficulty for daily challenge
  }
  
  static hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }
} 