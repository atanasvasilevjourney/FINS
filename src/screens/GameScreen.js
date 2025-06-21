import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  Alert,
  Modal,
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { useTheme } from '../context/ThemeContext';
import { 
  loadPuzzle, 
  submitWord, 
  clearSelection, 
  useHint, 
  pauseGame,
  resumeGame 
} from '../store/gameSlice';
import { addPoints, incrementGamesPlayed } from '../store/userSlice';
import CrosswordGrid from '../components/game/CrosswordGrid';
import ClueList from '../components/game/ClueList';
import Icon from 'react-native-vector-icons/MaterialIcons';

const GameScreen = () => {
  const dispatch = useDispatch();
  const theme = useTheme();
  const { 
    currentPuzzle, 
    selectedCells, 
    currentWord, 
    score, 
    hintsAvailable, 
    gameState,
    loading,
    error 
  } = useSelector(state => state.game);
  const { profile } = useSelector(state => state.user);
  
  const [showPauseModal, setShowPauseModal] = useState(false);
  const [timer, setTimer] = useState(0);
  
  useEffect(() => {
    if (!currentPuzzle && gameState === 'idle') {
      dispatch(loadPuzzle({ difficulty: 1, theme: 'nature' }));
    }
  }, [currentPuzzle, gameState, dispatch]);
  
  useEffect(() => {
    let interval;
    if (gameState === 'playing') {
      interval = setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [gameState]);
  
  const handleSubmitWord = () => {
    if (currentWord.length < 3) {
      Alert.alert('Грешка', 'Изберете поне 3 букви за да съставите дума.');
      return;
    }
    
    const positions = selectedCells.map(cell => {
      const [row, col] = cell.split('-').map(Number);
      return [row, col];
    });
    
    // Find matching clue
    const matchingClue = currentPuzzle.clues.find(clue => 
      clue.text === currentWord && !clue.solved
    );
    
    if (matchingClue) {
      dispatch(submitWord({
        word: currentWord,
        positions,
        clueId: matchingClue.id
      }));
    } else {
      Alert.alert('Грешка', 'Тази дума не съответства на никоя подсказка.');
    }
  };
  
  const handleUseHint = () => {
    if (hintsAvailable > 0) {
      const unsolvedClues = currentPuzzle.clues.filter(clue => !clue.solved);
      if (unsolvedClues.length > 0) {
        const randomClue = unsolvedClues[Math.floor(Math.random() * unsolvedClues.length)];
        dispatch(useHint({ clueId: randomClue.id }));
      }
    } else {
      Alert.alert('Няма подсказки', 'Използвахте всички налични подсказки.');
    }
  };
  
  const handlePause = () => {
    dispatch(pauseGame());
    setShowPauseModal(true);
  };
  
  const handleResume = () => {
    dispatch(resumeGame());
    setShowPauseModal(false);
  };
  
  const handleNewGame = () => {
    Alert.alert(
      'Нова игра',
      'Сигурни ли сте, че искате да започнете нова игра?',
      [
        { text: 'Отказ', style: 'cancel' },
        { 
          text: 'Да', 
          onPress: () => {
            dispatch(loadPuzzle({ difficulty: 1, theme: 'nature' }));
            setTimer(0);
            setShowPauseModal(false);
          }
        }
      ]
    );
  };
  
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: theme.spacing.md,
      backgroundColor: theme.colors.backgroundCard,
      borderBottomWidth: 1,
      borderBottomColor: theme.colors.border,
    },
    headerLeft: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    levelText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginRight: theme.spacing.md,
    },
    scoreText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.primary,
    },
    headerRight: {
      flexDirection: 'row',
      alignItems: 'center',
    },
    timerText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textSecondary,
      marginRight: theme.spacing.md,
    },
    hintButton: {
      backgroundColor: theme.colors.accent,
      padding: theme.spacing.sm,
      borderRadius: theme.borderRadius.round,
      marginRight: theme.spacing.sm,
    },
    hintCount: {
      position: 'absolute',
      top: -5,
      right: -5,
      backgroundColor: theme.colors.error,
      borderRadius: theme.borderRadius.round,
      width: 20,
      height: 20,
      justifyContent: 'center',
      alignItems: 'center',
    },
    hintCountText: {
      fontSize: 12,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
    pauseButton: {
      backgroundColor: theme.colors.warning,
      padding: theme.spacing.sm,
      borderRadius: theme.borderRadius.round,
    },
    content: {
      flex: 1,
      flexDirection: 'row',
    },
    leftPanel: {
      flex: 1,
      padding: theme.spacing.md,
    },
    rightPanel: {
      flex: 1,
      padding: theme.spacing.md,
    },
    currentWordContainer: {
      backgroundColor: theme.colors.backgroundCard,
      padding: theme.spacing.md,
      borderRadius: theme.borderRadius.medium,
      marginBottom: theme.spacing.md,
      ...theme.shadows.small,
    },
    currentWordLabel: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      marginBottom: theme.spacing.xs,
    },
    currentWordText: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      textAlign: 'center',
      letterSpacing: theme.typography.letterSpacing.medium,
    },
    actionButtons: {
      flexDirection: 'row',
      gap: theme.spacing.sm,
      marginBottom: theme.spacing.md,
    },
    actionButton: {
      flex: 1,
      padding: theme.spacing.md,
      borderRadius: theme.borderRadius.medium,
      alignItems: 'center',
    },
    clearButton: {
      backgroundColor: theme.colors.error,
    },
    submitButton: {
      backgroundColor: theme.colors.success,
    },
    actionButtonText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
    loadingContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
    },
    loadingText: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
    },
    pauseModal: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: theme.colors.backgroundOverlay,
    },
    pauseContent: {
      backgroundColor: theme.colors.backgroundCard,
      padding: theme.spacing.xl,
      borderRadius: theme.borderRadius.large,
      alignItems: 'center',
      ...theme.shadows.large,
    },
    pauseTitle: {
      fontSize: theme.typography.fontSize.title,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.lg,
    },
    pauseButtons: {
      flexDirection: 'row',
      gap: theme.spacing.md,
    },
    pauseButton: {
      paddingVertical: theme.spacing.md,
      paddingHorizontal: theme.spacing.lg,
      borderRadius: theme.borderRadius.medium,
      minWidth: 100,
      alignItems: 'center',
    },
    resumeButton: {
      backgroundColor: theme.colors.success,
    },
    newGameButton: {
      backgroundColor: theme.colors.primary,
    },
    pauseButtonText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
  });
  
  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Зареждане на пъзел...</Text>
      </View>
    );
  }
  
  if (error) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Грешка: {error}</Text>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => dispatch(loadPuzzle({ difficulty: 1, theme: 'nature' }))}
        >
          <Text style={styles.actionButtonText}>Опитайте отново</Text>
        </TouchableOpacity>
      </View>
    );
  }
  
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <Text style={styles.levelText}>Ниво {profile.level}</Text>
          <Text style={styles.scoreText}>{score} т.</Text>
        </View>
        
        <View style={styles.headerRight}>
          <Text style={styles.timerText}>{formatTime(timer)}</Text>
          
          <TouchableOpacity
            style={styles.hintButton}
            onPress={handleUseHint}
            disabled={hintsAvailable === 0}
          >
            <Icon name="lightbulb" size={24} color={theme.colors.textInverse} />
            {hintsAvailable > 0 && (
              <View style={styles.hintCount}>
                <Text style={styles.hintCountText}>{hintsAvailable}</Text>
              </View>
            )}
          </TouchableOpacity>
          
          <TouchableOpacity
            style={styles.pauseButton}
            onPress={handlePause}
          >
            <Icon name="pause" size={24} color={theme.colors.textInverse} />
          </TouchableOpacity>
        </View>
      </View>
      
      <View style={styles.content}>
        <View style={styles.leftPanel}>
          <CrosswordGrid />
          
          <View style={styles.currentWordContainer}>
            <Text style={styles.currentWordLabel}>Избрана дума:</Text>
            <Text style={styles.currentWordText}>
              {currentWord || 'Изберете букви от мрежата'}
            </Text>
          </View>
          
          <View style={styles.actionButtons}>
            <TouchableOpacity
              style={[styles.actionButton, styles.clearButton]}
              onPress={() => dispatch(clearSelection())}
            >
              <Text style={styles.actionButtonText}>Изчисти</Text>
            </TouchableOpacity>
            
            <TouchableOpacity
              style={[styles.actionButton, styles.submitButton]}
              onPress={handleSubmitWord}
              disabled={currentWord.length < 3}
            >
              <Text style={styles.actionButtonText}>Потвърди</Text>
            </TouchableOpacity>
          </View>
        </View>
        
        <View style={styles.rightPanel}>
          <ClueList />
        </View>
      </View>
      
      <Modal
        visible={showPauseModal}
        transparent
        animationType="fade"
      >
        <View style={styles.pauseModal}>
          <View style={styles.pauseContent}>
            <Text style={styles.pauseTitle}>Играта е на пауза</Text>
            
            <View style={styles.pauseButtons}>
              <TouchableOpacity
                style={[styles.pauseButton, styles.resumeButton]}
                onPress={handleResume}
              >
                <Text style={styles.pauseButtonText}>Продължи</Text>
              </TouchableOpacity>
              
              <TouchableOpacity
                style={[styles.pauseButton, styles.newGameButton]}
                onPress={handleNewGame}
              >
                <Text style={styles.pauseButtonText}>Нова игра</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
};

export default GameScreen; 