export class UserService {
  static async getProfile(userId) {
    // Mock implementation for demo
    return {
      id: userId,
      username: 'Играч',
      email: 'demo@example.com',
      profile: {
        totalPoints: 0,
        level: 1,
        gamesPlayed: 0,
        gamesCompleted: 0,
        totalTimePlayed: 0,
        averageAccuracy: 0,
        averageTime: 0,
        currentStreak: 0,
        longestStreak: 0,
        favoriteTheme: 'nature'
      },
      achievements: [],
      unlockedThemes: ['nature'],
      unlockedFonts: ['default'],
      unlockedBackgrounds: ['default'],
      dailyLoginStreak: 0,
      lastLoginDate: null
    };
  }
  
  static async updateStats(userId, gameResult) {
    // Mock implementation for demo
    return {
      totalPoints: gameResult.score || 0,
      gamesPlayed: 1,
      gamesCompleted: gameResult.completed ? 1 : 0,
      totalTimePlayed: gameResult.timeSpent || 0,
      averageAccuracy: gameResult.accuracy || 0,
      averageTime: gameResult.timeSpent || 0,
      currentStreak: gameResult.completed ? 1 : 0,
      longestStreak: gameResult.completed ? 1 : 0
    };
  }
  
  static async unlockAchievement(userId, achievementType, achievementData) {
    // Mock implementation for demo
    return {
      id: Date.now(),
      userId,
      achievement_type: achievementType,
      achievement_data: achievementData,
      unlocked_at: new Date().toISOString()
    };
  }
} 