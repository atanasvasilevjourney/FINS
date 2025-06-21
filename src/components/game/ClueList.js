import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useSelector, useDispatch } from 'react-redux';
import { useTheme } from '../../context/ThemeContext';
import Icon from 'react-native-vector-icons/MaterialIcons';

const ClueList = ({ onCluePress }) => {
  const theme = useTheme();
  const { currentPuzzle } = useSelector(state => state.game);
  
  if (!currentPuzzle || !currentPuzzle.clues) {
    return null;
  }
  
  const horizontalClues = currentPuzzle.clues.filter(clue => clue.direction === 'horizontal');
  const verticalClues = currentPuzzle.clues.filter(clue => clue.direction === 'vertical');
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      padding: theme.spacing.md,
    },
    section: {
      marginBottom: theme.spacing.lg,
    },
    sectionTitle: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.sm,
      paddingHorizontal: theme.spacing.sm,
    },
    clueContainer: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: theme.spacing.sm,
      marginVertical: 2,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.small,
      ...theme.shadows.small,
    },
    clueNumber: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.primary,
      marginRight: theme.spacing.sm,
      minWidth: 30,
      textAlign: 'center',
    },
    clueText: {
      flex: 1,
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
      lineHeight: theme.typography.lineHeight.medium * theme.typography.fontSize.medium,
    },
    solvedClueText: {
      color: theme.colors.textSecondary,
      textDecorationLine: 'line-through',
    },
    solvedIcon: {
      marginLeft: theme.spacing.sm,
      color: theme.colors.success,
    },
    directionIcon: {
      marginRight: theme.spacing.sm,
      color: theme.colors.primary,
    },
    emptyState: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      padding: theme.spacing.xl,
    },
    emptyText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
      textAlign: 'center',
    },
  });
  
  const renderClue = (clue, index) => (
    <TouchableOpacity
      key={clue.id}
      style={styles.clueContainer}
      onPress={() => onCluePress && onCluePress(clue)}
      activeOpacity={0.7}
    >
      <Icon
        name={clue.direction === 'horizontal' ? 'arrow-forward' : 'arrow-downward'}
        size={20}
        style={styles.directionIcon}
      />
      <Text style={styles.clueNumber}>{index + 1}</Text>
      <Text
        style={[
          styles.clueText,
          clue.solved && styles.solvedClueText,
        ]}
      >
        {clue.clue}
      </Text>
      {clue.solved && (
        <Icon
          name="check-circle"
          size={24}
          style={styles.solvedIcon}
        />
      )}
    </TouchableOpacity>
  );
  
  if (currentPuzzle.clues.length === 0) {
    return (
      <View style={styles.emptyState}>
        <Text style={styles.emptyText}>
          Няма налични подсказки за този пъзел.
        </Text>
      </View>
    );
  }
  
  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {horizontalClues.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Хоризонтални</Text>
          {horizontalClues.map((clue, index) => renderClue(clue, index))}
        </View>
      )}
      
      {verticalClues.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Вертикални</Text>
          {verticalClues.map((clue, index) => renderClue(clue, index))}
        </View>
      )}
    </ScrollView>
  );
};

export default ClueList; 