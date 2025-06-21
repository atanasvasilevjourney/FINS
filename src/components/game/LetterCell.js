import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { useTheme } from '../../context/ThemeContext';

const LetterCell = ({ letter, isSelected, isInWord, onPress, disabled }) => {
  const theme = useTheme();
  
  const styles = StyleSheet.create({
    cell: {
      width: 48,
      height: 48,
      justifyContent: 'center',
      alignItems: 'center',
      borderWidth: 1,
      borderColor: theme.colors.border,
      borderRadius: theme.borderRadius.small,
      backgroundColor: theme.colors.backgroundCard,
    },
    selected: {
      backgroundColor: theme.colors.primaryLight,
      borderColor: theme.colors.primary,
      borderWidth: 2,
    },
    inWord: {
      backgroundColor: theme.colors.backgroundSecondary,
    },
    letter: {
      fontSize: 20,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
    },
    selectedLetter: {
      color: theme.colors.textInverse,
    },
  });
  
  return (
    <TouchableOpacity
      style={[
        styles.cell,
        isSelected && styles.selected,
        isInWord && styles.inWord,
      ]}
      onPress={onPress}
      disabled={disabled}
      activeOpacity={0.7}
    >
      <Text style={[styles.letter, isSelected && styles.selectedLetter]}>
        {letter}
      </Text>
    </TouchableOpacity>
  );
};

export default LetterCell; 