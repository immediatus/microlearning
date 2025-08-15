/**
 * Typography Components for MicroLearning Platform
 * 
 * Age-adaptive text components with proper scaling
 * and accessibility features for educational content
 */

import React from 'react';
import {
  Text as RNText,
  TextStyle,
  TextProps as RNTextProps,
} from 'react-native';
import { Typography, Colors, AgeGroups, type AgeGroup } from './DesignSystem';

interface TextProps extends RNTextProps {
  variant?: 'hero' | 'h1' | 'h2' | 'h3' | 'body' | 'bodyLarge' | 'caption' | 'small';
  ageGroup?: AgeGroup;
  color?: string;
  align?: 'left' | 'center' | 'right' | 'justify';
  weight?: 'light' | 'regular' | 'medium' | 'semibold' | 'bold';
  children: React.ReactNode;
  style?: TextStyle;
  numberOfLines?: number;
  adjustsFontSizeToFit?: boolean;
  minimumFontScale?: number;
}

export const Text: React.FC<TextProps> = ({
  variant = 'body',
  ageGroup = '12-15',
  color = Colors.neutral.textPrimary,
  align = 'left',
  weight,
  children,
  style,
  numberOfLines,
  adjustsFontSizeToFit = false,
  minimumFontScale = 0.8,
  ...props
}) => {
  const ageConfig = AgeGroups[ageGroup];
  const variantConfig = Typography.mobile[variant];
  
  // Apply age-specific font size adjustments
  const adjustedFontSize = variantConfig.fontSize * ageConfig.fontSize;
  
  const textStyle: TextStyle = {
    fontSize: adjustedFontSize,
    fontWeight: weight ? Typography.weights[weight] : variantConfig.fontWeight,
    lineHeight: variantConfig.lineHeight * ageConfig.fontSize,
    letterSpacing: variantConfig.letterSpacing,
    color,
    textAlign: align,
    ...style,
  };

  return (
    <RNText
      style={textStyle}
      numberOfLines={numberOfLines}
      adjustsFontSizeToFit={adjustsFontSizeToFit}
      minimumFontScale={minimumFontScale}
      accessibilityRole="text"
      {...props}
    >
      {children}
    </RNText>
  );
};

// Specialized text components for common use cases
export const Heading: React.FC<Omit<TextProps, 'variant'> & {
  level: 1 | 2 | 3;
}> = ({ level, weight = 'semibold', ...props }) => {
  const variantMap = {
    1: 'h1' as const,
    2: 'h2' as const,
    3: 'h3' as const,
  };

  return (
    <Text
      variant={variantMap[level]}
      weight={weight}
      {...props}
    />
  );
};

export const Title: React.FC<Omit<TextProps, 'variant'>> = ({ weight = 'bold', ...props }) => {
  return (
    <Text
      variant="hero"
      weight={weight}
      {...props}
    />
  );
};

export const Body: React.FC<Omit<TextProps, 'variant'>> = ({ ...props }) => {
  return (
    <Text
      variant="body"
      {...props}
    />
  );
};

export const Caption: React.FC<Omit<TextProps, 'variant'>> = ({ 
  color = Colors.neutral.textSecondary,
  ...props 
}) => {
  return (
    <Text
      variant="caption"
      color={color}
      {...props}
    />
  );
};

export const QuestionText: React.FC<Omit<TextProps, 'variant'>> = ({ 
  align = 'center',
  weight = 'semibold',
  ...props 
}) => {
  return (
    <Text
      variant="h2"
      align={align}
      weight={weight}
      adjustsFontSizeToFit={true}
      numberOfLines={3}
      {...props}
    />
  );
};

export const FeedbackText: React.FC<Omit<TextProps, 'variant'> & {
  type: 'correct' | 'incorrect' | 'neutral';
}> = ({ type, color, weight = 'semibold', ...props }) => {
  const typeColors = {
    correct: Colors.interactive.correct,
    incorrect: Colors.interactive.incorrect,
    neutral: Colors.neutral.textPrimary,
  };

  return (
    <Text
      variant="bodyLarge"
      color={color || typeColors[type]}
      weight={weight}
      align="center"
      {...props}
    />
  );
};

export const CountdownText: React.FC<Omit<TextProps, 'variant'> & {
  timeLeft: number;
  maxTime: number;
}> = ({ timeLeft, maxTime, ...props }) => {
  const isUrgent = timeLeft < maxTime * 0.3; // Last 30% of time
  const urgentColor = isUrgent ? Colors.semantic.error : Colors.neutral.textPrimary;

  return (
    <Text
      variant="h3"
      color={urgentColor}
      weight="bold"
      align="center"
      {...props}
    >
      {Math.ceil(timeLeft / 1000)}
    </Text>
  );
};

export const ProgressText: React.FC<Omit<TextProps, 'variant'> & {
  current: number;
  total: number;
}> = ({ current, total, ...props }) => {
  return (
    <Text
      variant="caption"
      weight="medium"
      {...props}
    >
      {current} of {total}
    </Text>
  );
};

export const ScoreText: React.FC<Omit<TextProps, 'variant'> & {
  score: number;
  maxScore: number;
  showPercentage?: boolean;
}> = ({ score, maxScore, showPercentage = true, ...props }) => {
  const percentage = Math.round((score / maxScore) * 100);
  const displayText = showPercentage ? `${percentage}%` : `${score}/${maxScore}`;

  return (
    <Text
      variant="h2"
      weight="bold"
      align="center"
      {...props}
    >
      {displayText}
    </Text>
  );
};

export const InstructionText: React.FC<Omit<TextProps, 'variant'>> = ({ 
  color = Colors.neutral.textSecondary,
  align = 'center',
  ...props 
}) => {
  return (
    <Text
      variant="caption"
      color={color}
      align={align}
      {...props}
    />
  );
};

// Accessibility-enhanced text for screen readers
export const AccessibleText: React.FC<TextProps & {
  accessibilityLabel?: string;
  accessibilityHint?: string;
  accessibilityLiveRegion?: 'none' | 'polite' | 'assertive';
}> = ({ 
  accessibilityLabel,
  accessibilityHint,
  accessibilityLiveRegion = 'none',
  children,
  ...props 
}) => {
  return (
    <Text
      accessibilityLabel={accessibilityLabel}
      accessibilityHint={accessibilityHint}
      accessibilityLiveRegion={accessibilityLiveRegion}
      {...props}
    >
      {children}
    </Text>
  );
};

// Animated text for dynamic content
export const AnimatedText: React.FC<TextProps & {
  animationType?: 'fadeIn' | 'slideUp' | 'bounce';
  delay?: number;
}> = ({ animationType = 'fadeIn', delay = 0, children, ...props }) => {
  // Animation logic would be implemented here
  // For now, just render the text
  return (
    <Text {...props}>
      {children}
    </Text>
  );
};