import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useTheme } from '../context/ThemeContext';
import Icon from 'react-native-vector-icons/MaterialIcons';

const LeaderboardScreen = () => {
  const theme = useTheme();
  
  // Mock leaderboard data
  const leaderboardData = [
    { id: 1, username: 'Играч1', score: 12500, level: 15, games: 45 },
    { id: 2, username: 'Играч2', score: 11800, level: 14, games: 42 },
    { id: 3, username: 'Играч3', score: 11200, level: 13, games: 38 },
    { id: 4, username: 'Играч4', score: 10500, level: 12, games: 35 },
    { id: 5, username: 'Играч5', score: 9800, level: 11, games: 32 },
    { id: 6, username: 'Играч6', score: 9200, level: 10, games: 28 },
    { id: 7, username: 'Играч7', score: 8700, level: 9, games: 25 },
    { id: 8, username: 'Играч8', score: 8200, level: 8, games: 22 },
    { id: 9, username: 'Играч9', score: 7800, level: 7, games: 20 },
    { id: 10, username: 'Играч10', score: 7400, level: 6, games: 18 },
  ];
  
  const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    content: {
      padding: theme.spacing.md,
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: theme.spacing.lg,
    },
    title: {
      fontSize: theme.typography.fontSize.title,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
    },
    filterButton: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: theme.spacing.sm,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      ...theme.shadows.small,
    },
    filterText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.text,
      marginLeft: theme.spacing.sm,
    },
    leaderboardItem: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: theme.spacing.md,
      backgroundColor: theme.colors.backgroundCard,
      borderRadius: theme.borderRadius.medium,
      marginBottom: theme.spacing.sm,
      ...theme.shadows.small,
    },
    rankContainer: {
      width: 40,
      height: 40,
      borderRadius: theme.borderRadius.round,
      justifyContent: 'center',
      alignItems: 'center',
      marginRight: theme.spacing.md,
    },
    rank1: {
      backgroundColor: '#FFD700', // Gold
    },
    rank2: {
      backgroundColor: '#C0C0C0', // Silver
    },
    rank3: {
      backgroundColor: '#CD7F32', // Bronze
    },
    rankOther: {
      backgroundColor: theme.colors.primaryLight,
    },
    rankText: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.textInverse,
    },
    playerInfo: {
      flex: 1,
    },
    playerName: {
      fontSize: theme.typography.fontSize.medium,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.text,
      marginBottom: 2,
    },
    playerStats: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
    },
    scoreContainer: {
      alignItems: 'flex-end',
    },
    score: {
      fontSize: theme.typography.fontSize.large,
      fontFamily: theme.typography.fontFamilyBold,
      color: theme.colors.primary,
      marginBottom: 2,
    },
    level: {
      fontSize: theme.typography.fontSize.small,
      fontFamily: theme.typography.fontFamily,
      color: theme.colors.textSecondary,
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
  
  const getRankStyle = (rank) => {
    switch (rank) {
      case 1:
        return styles.rank1;
      case 2:
        return styles.rank2;
      case 3:
        return styles.rank3;
      default:
        return styles.rankOther;
    }
  };
  
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>Класация</Text>
        <TouchableOpacity style={styles.filterButton}>
          <Icon name="filter-list" size={20} color={theme.colors.primary} />
          <Text style={styles.filterText}>Топ 10</Text>
        </TouchableOpacity>
      </View>
      
      {leaderboardData.map((player, index) => (
        <View key={player.id} style={styles.leaderboardItem}>
          <View style={[styles.rankContainer, getRankStyle(index + 1)]}>
            <Text style={styles.rankText}>{index + 1}</Text>
          </View>
          
          <View style={styles.playerInfo}>
            <Text style={styles.playerName}>{player.username}</Text>
            <Text style={styles.playerStats}>
              {player.games} игри • Ниво {player.level}
            </Text>
          </View>
          
          <View style={styles.scoreContainer}>
            <Text style={styles.score}>{player.score.toLocaleString()}</Text>
            <Text style={styles.level}>точки</Text>
          </View>
        </View>
      ))}
    </ScrollView>
  );
};

export default LeaderboardScreen; 