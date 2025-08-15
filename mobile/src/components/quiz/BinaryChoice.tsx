/**
 * Binary Choice Quiz Component
 * 
 * Optimized for mobile with large touch zones and immediate feedback
 * Supports the rapid-fire quiz interactions for educational content
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  ViewStyle,
  Animated,
  Vibration,
  PanGestureHandler,
  State,
} from 'react-native';
import { Colors, Spacing, AgeGroups, type AgeGroup } from '../ui/DesignSystem';
import { Text, QuestionText, FeedbackText, InstructionText } from '../ui/Typography';
import { BinaryChoiceButton } from '../ui/Button';

interface BinaryChoiceProps {
  question: string;
  correctAnswer: boolean;
  timeLimit?: number; // in milliseconds
  ageGroup?: AgeGroup;
  onAnswer: (answer: boolean, isCorrect: boolean, responseTime: number) => void;
  onTimeout?: () => void;
  showInstructions?: boolean;
  hapticFeedback?: boolean;
  autoAdvance?: boolean;
  autoAdvanceDelay?: number;
}

type AnswerState = 'pending' | 'correct' | 'incorrect' | 'timeout';

export const BinaryChoice: React.FC<BinaryChoiceProps> = ({
  question,
  correctAnswer,
  timeLimit = 5000,
  ageGroup = '12-15',
  onAnswer,
  onTimeout,
  showInstructions = true,
  hapticFeedback = true,
  autoAdvance = true,
  autoAdvanceDelay = 1500,
}) => {
  const [answerState, setAnswerState] = useState<AnswerState>('pending');
  const [timeLeft, setTimeLeft] = useState(timeLimit);
  const [startTime] = useState(Date.now());
  
  // Animation values
  const fadeAnim = React.useRef(new Animated.Value(0)).current;
  const scaleAnim = React.useRef(new Animated.Value(0.9)).current;
  const leftZoneAnim = React.useRef(new Animated.Value(1)).current;
  const rightZoneAnim = React.useRef(new Animated.Value(1)).current;
  const progressAnim = React.useRef(new Animated.Value(1)).current;
  
  const ageConfig = AgeGroups[ageGroup];

  // Initialize animations
  useEffect(() => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 300,
        useNativeDriver: true,
      }),
      Animated.spring(scaleAnim, {
        toValue: 1,
        tension: 100,
        friction: 8,
        useNativeDriver: true,
      }),
    ]).start();
  }, []);

  // Timer countdown
  useEffect(() => {
    if (answerState !== 'pending') return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        const newTime = prev - 100;
        
        // Update progress animation
        Animated.timing(progressAnim, {
          toValue: newTime / timeLimit,
          duration: 100,
          useNativeDriver: false,
        }).start();
        
        if (newTime <= 0) {
          handleTimeout();
          return 0;
        }
        return newTime;
      });
    }, 100);

    return () => clearInterval(timer);
  }, [answerState, timeLimit]);

  const handleTimeout = () => {
    if (answerState !== 'pending') return;
    
    setAnswerState('timeout');
    if (hapticFeedback) {
      Vibration.vibrate([100, 50, 100]);
    }
    
    onTimeout?.();
    
    if (autoAdvance) {
      setTimeout(() => {
        // Auto-advance logic would be handled by parent
      }, autoAdvanceDelay);
    }
  };

  const handleAnswer = (userAnswer: boolean) => {
    if (answerState !== 'pending') return;
    
    const responseTime = Date.now() - startTime;
    const isCorrect = userAnswer === correctAnswer;
    const newState: AnswerState = isCorrect ? 'correct' : 'incorrect';
    
    setAnswerState(newState);
    
    // Haptic feedback
    if (hapticFeedback) {
      if (isCorrect) {
        Vibration.vibrate(100); // Single buzz for correct
      } else {
        Vibration.vibrate([100, 100, 100]); // Triple buzz for incorrect
      }
    }
    
    // Visual feedback animation
    const targetZone = userAnswer ? rightZoneAnim : leftZoneAnim;
    Animated.sequence([
      Animated.timing(targetZone, {
        toValue: 1.1,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(targetZone, {
        toValue: 1,
        duration: 200,
        useNativeDriver: true,
      }),
    ]).start();
    
    onAnswer(userAnswer, isCorrect, responseTime);
    
    if (autoAdvance) {
      setTimeout(() => {
        // Auto-advance logic would be handled by parent
      }, autoAdvanceDelay);
    }
  };

  const getFeedbackMessage = (): string => {
    switch (answerState) {
      case 'correct':
        return 'Correct! 🎉';
      case 'incorrect':
        return 'Not quite! 💭';
      case 'timeout':
        return 'Time\'s up! ⏰';
      default:
        return '';
    }
  };

  const getProgressColor = (): string => {
    const progress = timeLeft / timeLimit;
    if (progress > 0.6) return Colors.interactive.correct;
    if (progress > 0.3) return Colors.primary.orange;
    return Colors.interactive.incorrect;
  };

  const containerStyle: ViewStyle = {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.lg * ageConfig.spacing,
    backgroundColor: Colors.neutral.backgroundLight,
  };

  const questionContainerStyle: ViewStyle = {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: Spacing.xl,
  };

  const choiceContainerStyle: ViewStyle = {
    flexDirection: 'row',
    width: '100%',
    height: ageConfig.touchTargetSize * 2,
    gap: Spacing.sm,
  };

  const progressBarStyle: ViewStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 4,
    backgroundColor: Colors.neutral.border,
  };

  return (
    <Animated.View
      style={[
        containerStyle,
        {
          opacity: fadeAnim,
          transform: [{ scale: scaleAnim }],
        },
      ]}
    >
      {/* Progress bar */}
      <View style={progressBarStyle}>
        <Animated.View
          style={{
            width: progressAnim.interpolate({
              inputRange: [0, 1],
              outputRange: ['0%', '100%'],
            }),
            height: '100%',
            backgroundColor: getProgressColor(),
          }}
        />
      </View>

      {/* Question section */}
      <View style={questionContainerStyle}>
        <QuestionText ageGroup={ageGroup}>
          {question}
        </QuestionText>
        
        {showInstructions && answerState === 'pending' && (
          <InstructionText style={{ marginTop: Spacing.md }}>
            Tap left for NO • Tap right for YES
          </InstructionText>
        )}
        
        {answerState !== 'pending' && (
          <FeedbackText
            type={answerState === 'correct' ? 'correct' : 'incorrect'}
            style={{ marginTop: Spacing.md }}
          >
            {getFeedbackMessage()}
          </FeedbackText>
        )}
      </View>

      {/* Choice buttons */}
      <Animated.View style={choiceContainerStyle}>
        <Animated.View
          style={{
            flex: 1,
            transform: [{ scale: leftZoneAnim }],
          }}
        >
          <BinaryChoiceButton
            choice="no"
            zone="left"
            ageGroup={ageGroup}
            onPress={() => handleAnswer(false)}
            disabled={answerState !== 'pending'}
            style={{
              backgroundColor: answerState === 'pending' 
                ? Colors.interactive.incorrect 
                : answerState === 'correct' && !correctAnswer
                  ? Colors.interactive.correct
                  : Colors.interactive.incorrect,
            }}
          >
            <Text variant="h2" color={Colors.neutral.textInverse} weight="bold">
              NO
            </Text>
          </BinaryChoiceButton>
        </Animated.View>

        <Animated.View
          style={{
            flex: 1,
            transform: [{ scale: rightZoneAnim }],
          }}
        >
          <BinaryChoiceButton
            choice="yes"
            zone="right"
            ageGroup={ageGroup}
            onPress={() => handleAnswer(true)}
            disabled={answerState !== 'pending'}
            style={{
              backgroundColor: answerState === 'pending'
                ? Colors.interactive.correct
                : answerState === 'correct' && correctAnswer
                  ? Colors.interactive.correct
                  : Colors.interactive.incorrect,
            }}
          >
            <Text variant="h2" color={Colors.neutral.textInverse} weight="bold">
              YES
            </Text>
          </BinaryChoiceButton>
        </Animated.View>
      </Animated.View>

      {/* Timer display */}
      {answerState === 'pending' && (
        <View style={{
          position: 'absolute',
          top: Spacing.xl,
          right: Spacing.xl,
          width: 60,
          height: 60,
          borderRadius: 30,
          backgroundColor: Colors.neutral.backgroundLight,
          borderWidth: 3,
          borderColor: getProgressColor(),
          alignItems: 'center',
          justifyContent: 'center',
          shadowColor: Colors.neutral.shadow,
          shadowOffset: { width: 0, height: 2 },
          shadowOpacity: 0.1,
          shadowRadius: 4,
          elevation: 4,
        }}>
          <Text variant="body" weight="bold" color={getProgressColor()}>
            {Math.ceil(timeLeft / 1000)}
          </Text>
        </View>
      )}
    </Animated.View>
  );
};

// Rapid-fire variant for sequential questions
export const RapidFireBinaryChoice: React.FC<BinaryChoiceProps & {
  questionNumber: number;
  totalQuestions: number;
}> = ({ questionNumber, totalQuestions, ...props }) => {
  return (
    <View style={{ flex: 1 }}>
      {/* Progress indicator */}
      <View style={{
        flexDirection: 'row',
        justifyContent: 'center',
        padding: Spacing.md,
        gap: Spacing.xs,
      }}>
        {Array.from({ length: totalQuestions }, (_, index) => (
          <View
            key={index}
            style={{
              width: 8,
              height: 8,
              borderRadius: 4,
              backgroundColor: index < questionNumber
                ? Colors.interactive.correct
                : index === questionNumber
                  ? Colors.primary.blue
                  : Colors.neutral.border,
            }}
          />
        ))}
      </View>
      
      <BinaryChoice {...props} />
    </View>
  );
};