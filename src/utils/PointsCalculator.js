export class PointsCalculator {
  static calculateWordPoints(word, timeSpent, hintsUsed, difficulty) {
    let basePoints = word.length * 10;
    
    // Time bonus (faster = more points)
    const timeBonus = Math.max(0, 60 - timeSpent) * 2;
    
    // Difficulty multiplier
    const difficultyMultiplier = {
      1: 1.0, 2: 1.2, 3: 1.5, 4: 1.8, 5: 2.0
    };
    
    // Hint penalty
    const hintPenalty = hintsUsed * 5;
    
    // Word complexity bonus
    const complexityBonus = this.calculateComplexityBonus(word);
    
    const totalPoints = Math.floor(
      (basePoints + timeBonus + complexityBonus) * difficultyMultiplier[difficulty] - hintPenalty
    );
    
    return Math.max(totalPoints, 5); // Minimum 5 points
  }
  
  static calculatePuzzleBonus(completionTime, perfectSolve, hintsUsed, difficulty) {
    let bonus = 0;
    
    // Perfect solve bonus
    if (perfectSolve) bonus += 100;
    
    // Speed bonus
    if (completionTime < 300) bonus += 50; // Under 5 minutes
    if (completionTime < 180) bonus += 100; // Under 3 minutes
    if (completionTime < 120) bonus += 200; // Under 2 minutes
    
    // No hints bonus
    if (hintsUsed === 0) bonus += 50;
    
    // Difficulty bonus
    const difficultyBonus = {
      1: 0, 2: 25, 3: 50, 4: 75, 5: 100
    };
    bonus += difficultyBonus[difficulty] || 0;
    
    return bonus;
  }
  
  static calculateComplexityBonus(word) {
    let bonus = 0;
    
    // Length bonus
    if (word.length > 8) bonus += 20;
    if (word.length > 12) bonus += 30;
    
    // Rare letters bonus
    const rareLetters = ['Ж', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ь'];
    const rareCount = word.split('').filter(letter => rareLetters.includes(letter)).length;
    bonus += rareCount * 5;
    
    // Palindrome bonus
    if (this.isPalindrome(word)) bonus += 50;
    
    // Repeated letters penalty
    const letterCounts = {};
    word.split('').forEach(letter => {
      letterCounts[letter] = (letterCounts[letter] || 0) + 1;
    });
    
    const maxRepeats = Math.max(...Object.values(letterCounts));
    if (maxRepeats > 2) {
      bonus -= (maxRepeats - 2) * 5;
    }
    
    return bonus;
  }
  
  static isPalindrome(word) {
    const normalized = word.toUpperCase().replace(/\s/g, '');
    return normalized === normalized.split('').reverse().join('');
  }
  
  static calculateDailyChallengeBonus(completionTime, hintsUsed, streak) {
    let bonus = 0;
    
    // Base daily challenge bonus
    bonus += 100;
    
    // Speed bonus for daily challenge
    if (completionTime < 600) bonus += 50; // Under 10 minutes
    if (completionTime < 300) bonus += 100; // Under 5 minutes
    
    // Streak bonus
    if (streak > 0) {
      bonus += Math.min(streak * 10, 100); // Max 100 points for streak
    }
    
    // No hints bonus
    if (hintsUsed === 0) bonus += 25;
    
    return bonus;
  }
  
  static calculateLevelUpBonus(newLevel) {
    // Bonus points for reaching new levels
    const levelBonuses = {
      5: 100,
      10: 200,
      25: 500,
      50: 1000,
      100: 2000
    };
    
    return levelBonuses[newLevel] || 0;
  }
  
  static calculateAchievementBonus(achievementType) {
    const achievementBonuses = {
      'first_win': 50,
      'perfect_solve': 100,
      'speed_demon': 75,
      'no_hints': 50,
      'streak_7': 200,
      'streak_30': 500,
      'theme_master': 150,
      'word_collector': 100,
      'daily_champion': 300,
      'puzzle_master': 500
    };
    
    return achievementBonuses[achievementType] || 0;
  }
  
  static calculateStreakBonus(currentStreak) {
    if (currentStreak <= 1) return 0;
    
    // Exponential bonus for streaks
    return Math.floor(Math.pow(currentStreak, 1.5) * 5);
  }
  
  static calculateAccuracyBonus(accuracy) {
    if (accuracy >= 0.95) return 50;
    if (accuracy >= 0.90) return 25;
    if (accuracy >= 0.80) return 10;
    return 0;
  }
  
  static calculateTimeBonus(timeSpent, estimatedTime) {
    const timeRatio = timeSpent / estimatedTime;
    
    if (timeRatio <= 0.5) return 100; // Very fast
    if (timeRatio <= 0.75) return 50; // Fast
    if (timeRatio <= 1.0) return 25; // On time
    if (timeRatio <= 1.5) return 0; // Slightly slow
    return -25; // Very slow
  }
  
  static calculateThemeBonus(theme, userPreference) {
    if (theme === userPreference) return 25;
    return 0;
  }
  
  static calculateTotalScore(wordPoints, puzzleBonus, dailyBonus, levelBonus, achievementBonus, streakBonus, accuracyBonus, timeBonus, themeBonus) {
    return wordPoints + puzzleBonus + dailyBonus + levelBonus + achievementBonus + streakBonus + accuracyBonus + timeBonus + themeBonus;
  }
  
  static getScoreMultiplier(combo) {
    // Combo multiplier for consecutive correct answers
    if (combo <= 1) return 1.0;
    if (combo <= 3) return 1.1;
    if (combo <= 5) return 1.2;
    if (combo <= 10) return 1.5;
    return 2.0;
  }
  
  static calculateComboBonus(combo) {
    if (combo <= 1) return 0;
    return Math.floor(combo * 5);
  }
} 