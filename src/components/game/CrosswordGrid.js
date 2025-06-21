import React from 'react';
import {
  View,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  Text,
  Animated,
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { selectCell } from '../../store/gameSlice';
import { useTheme } from '../../context/ThemeContext';
import LetterCell from './LetterCell';

const { width: screenWidth } = Dimensions.get('window');

const CrosswordGrid = () => {
  const dispatch = useDispatch();
  const theme = useTheme();
  const { currentPuzzle, selectedCells, gameState } = useSelector(state => state.game);
  
  if (!currentPuzzle) {
    return null;
  }
  
  const gridSize = currentPuzzle.size;
  const cellSize = Math.min((screenWidth - 40) / gridSize.cols, 50);
  const gridWidth = cellSize * gridSize.cols;
  const gridHeight = cellSize * gridSize.rows;
  
  const handleCellPress = (row, col) => {
    if (gameState === 'playing') {
      dispatch(selectCell({ row, col }));
    }
  };
  
  const isCellSelected = (row, col) => {
    return selectedCells.includes(`${row}-${col}`);
  };
  
  const isCellInWord = (row, col) => {
    const cell = currentPuzzle.letters[row][col];
    return cell && cell.used;
  };
  
  const styles = StyleSheet.create({
    container: {
      alignItems: 'center',
      padding: theme.spacing.md,
    },
    gridContainer: {
      width: gridWidth,
      height: gridHeight,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      ...theme.shadows.medium,
      overflow: 'hidden',
    },
    grid: {
      flex: 1,
      flexDirection: 'row',
      flexWrap: 'wrap',
    },
    row: {
      flexDirection: 'row',
    },
    cell: {
      width: cellSize,
      height: cellSize,
      justifyContent: 'center',
      alignItems: 'center',
      borderWidth: 0.5,
      borderColor: theme.colors.borderLight,
    },
    selectedCell: {
      backgroundColor: theme.colors.primaryLight,
      borderColor: theme.colors.primary,
      borderWidth: 2,
    },
    wordCell: {
      backgroundColor: theme.colors.backgroundSecondary,
    },
    letterText: {
      fontSize: Math.max(cellSize * 0.4, 16),
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      textAlign: 'center',
    },
    selectedLetterText: {
      color: theme.colors.textInverse,
    },
    wordLetterText: {
      color: theme.colors.text,
    },
    emptyCell: {
      backgroundColor: theme.colors.background,
    },
  });
  
  return (
    <View style={styles.container}>
      <View style={styles.gridContainer}>
        <View style={styles.grid}>
          {currentPuzzle.letters.map((row, rowIndex) => (
            <View key={rowIndex} style={styles.row}>
              {row.map((cell, colIndex) => {
                const isSelected = isCellSelected(rowIndex, colIndex);
                const isInWord = isCellInWord(rowIndex, colIndex);
                const isEmpty = !cell.letter;
                
                return (
                  <TouchableOpacity
                    key={`${rowIndex}-${colIndex}`}
                    style={[
                      styles.cell,
                      isSelected && styles.selectedCell,
                      isInWord && styles.wordCell,
                      isEmpty && styles.emptyCell,
                    ]}
                    onPress={() => handleCellPress(rowIndex, colIndex)}
                    activeOpacity={0.7}
                    disabled={isEmpty || gameState !== 'playing'}
                  >
                    {!isEmpty && (
                      <Text
                        style={[
                          styles.letterText,
                          isSelected && styles.selectedLetterText,
                          isInWord && styles.wordLetterText,
                        ]}
                      >
                        {cell.letter}
                      </Text>
                    )}
                  </TouchableOpacity>
                );
              })}
            </View>
          ))}
        </View>
      </View>
    </View>
  );
};

export default CrosswordGrid; 