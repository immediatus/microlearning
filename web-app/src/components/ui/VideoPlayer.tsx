/**
 * Video Player Component for MicroLearning Web App
 * 
 * Mobile-optimized video player with 9:16 aspect ratio support,
 * custom controls, and educational content features
 */

import React, { useRef, useEffect, useState, useCallback } from 'react';
import { cn } from '@/lib/utils';
import { Play, Pause, Volume2, VolumeX, Maximize, SkipForward } from 'lucide-react';
import { Button } from './Button';

interface VideoPlayerProps {
  src: string;
  poster?: string;
  title?: string;
  duration?: number;
  onProgress?: (progress: number) => void;
  onComplete?: () => void;
  onTimeUpdate?: (currentTime: number, duration: number) => void;
  onLoadStart?: () => void;
  onLoadEnd?: () => void;
  autoPlay?: boolean;
  muted?: boolean;
  className?: string;
  controls?: boolean;
  aspectRatio?: '16:9' | '9:16' | '4:3' | '1:1';
  ageGroup?: '5-8' | '9-11' | '12-15';
  showSkipButton?: boolean;
  onSkip?: () => void;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({
  src,
  poster,
  title,
  duration,
  onProgress,
  onComplete,
  onTimeUpdate,
  onLoadStart,
  onLoadEnd,
  autoPlay = false,
  muted = false,
  className,
  controls = true,
  aspectRatio = '9:16',
  ageGroup = '12-15',
  showSkipButton = false,
  onSkip,
}) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(muted);
  const [currentTime, setCurrentTime] = useState(0);
  const [videoDuration, setVideoDuration] = useState(duration || 0);
  const [isLoading, setIsLoading] = useState(true);
  const [showControls, setShowControls] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  
  // Touch/click timeout for hiding controls
  const controlsTimeoutRef = useRef<NodeJS.Timeout>();

  // Aspect ratio classes
  const aspectRatioClasses = {
    '16:9': 'aspect-video', // Standard landscape
    '9:16': 'aspect-[9/16]', // TikTok-style portrait
    '4:3': 'aspect-[4/3]', // Traditional TV
    '1:1': 'aspect-square', // Square format
  };

  // Age-specific control sizes
  const ageControlSizes = {
    '5-8': 'h-12 w-12 text-lg', // Larger for younger kids
    '9-11': 'h-10 w-10 text-base',
    '12-15': 'h-9 w-9 text-sm', // Standard
  };

  // Initialize video event listeners
  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleLoadStart = () => {
      setIsLoading(true);
      onLoadStart?.();
    };

    const handleLoadedData = () => {
      setIsLoading(false);
      setVideoDuration(video.duration);
      onLoadEnd?.();
    };

    const handleTimeUpdate = () => {
      const current = video.currentTime;
      const total = video.duration;
      setCurrentTime(current);
      
      if (total > 0) {
        const progress = current / total;
        onProgress?.(progress);
        onTimeUpdate?.(current, total);
      }
    };

    const handleEnded = () => {
      setIsPlaying(false);
      onComplete?.();
    };

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);

    // Add event listeners
    video.addEventListener('loadstart', handleLoadStart);
    video.addEventListener('loadeddata', handleLoadedData);
    video.addEventListener('timeupdate', handleTimeUpdate);
    video.addEventListener('ended', handleEnded);
    video.addEventListener('play', handlePlay);
    video.addEventListener('pause', handlePause);

    return () => {
      video.removeEventListener('loadstart', handleLoadStart);
      video.removeEventListener('loadeddata', handleLoadedData);
      video.removeEventListener('timeupdate', handleTimeUpdate);
      video.removeEventListener('ended', handleEnded);
      video.removeEventListener('play', handlePlay);
      video.removeEventListener('pause', handlePause);
    };
  }, [onProgress, onComplete, onTimeUpdate, onLoadStart, onLoadEnd]);

  // Auto-hide controls
  useEffect(() => {
    if (!controls) return;

    const resetTimeout = () => {
      if (controlsTimeoutRef.current) {
        clearTimeout(controlsTimeoutRef.current);
      }
      
      setShowControls(true);
      
      if (isPlaying) {
        controlsTimeoutRef.current = setTimeout(() => {
          setShowControls(false);
        }, 3000);
      }
    };

    resetTimeout();

    return () => {
      if (controlsTimeoutRef.current) {
        clearTimeout(controlsTimeoutRef.current);
      }
    };
  }, [isPlaying, controls]);

  // Fullscreen handling
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  const togglePlayPause = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;

    if (isPlaying) {
      video.pause();
    } else {
      video.play();
    }
  }, [isPlaying]);

  const toggleMute = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;

    video.muted = !video.muted;
    setIsMuted(video.muted);
  }, []);

  const toggleFullscreen = useCallback(async () => {
    const container = videoRef.current?.parentElement;
    if (!container) return;

    try {
      if (!document.fullscreenElement) {
        await container.requestFullscreen();
      } else {
        await document.exitFullscreen();
      }
    } catch (error) {
      console.error('Fullscreen error:', error);
    }
  }, []);

  const handleProgressClick = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
    const video = videoRef.current;
    const progressBar = progressRef.current;
    if (!video || !progressBar) return;

    const rect = progressBar.getBoundingClientRect();
    const clickX = event.clientX - rect.left;
    const progressWidth = rect.width;
    const clickProgress = clickX / progressWidth;
    
    video.currentTime = clickProgress * video.duration;
  }, []);

  const handleVideoClick = useCallback(() => {
    togglePlayPause();
    // Show controls temporarily
    setShowControls(true);
  }, [togglePlayPause]);

  const formatTime = (time: number): string => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const progressPercentage = videoDuration > 0 ? (currentTime / videoDuration) * 100 : 0;

  return (
    <div 
      className={cn(
        'relative bg-black rounded-lg overflow-hidden shadow-lg',
        aspectRatioClasses[aspectRatio],
        isFullscreen && 'rounded-none',
        className
      )}
      onMouseEnter={() => setShowControls(true)}
      onMouseLeave={() => isPlaying && setShowControls(false)}
      onTouchStart={() => setShowControls(true)}
    >
      {/* Video element */}
      <video
        ref={videoRef}
        className="w-full h-full object-cover cursor-pointer"
        src={src}
        poster={poster}
        autoPlay={autoPlay}
        muted={muted}
        playsInline
        preload="metadata"
        onClick={handleVideoClick}
        onDoubleClick={toggleFullscreen}
        aria-label={title || 'Educational video'}
      />

      {/* Loading indicator */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white"></div>
        </div>
      )}

      {/* Skip button (top-right) */}
      {showSkipButton && onSkip && (
        <Button
          onClick={onSkip}
          variant="ghost"
          size="sm"
          className={cn(
            'absolute top-4 right-4 bg-black bg-opacity-50 text-white hover:bg-opacity-70',
            ageControlSizes[ageGroup]
          )}
          aria-label="Skip video"
        >
          <SkipForward className="h-4 w-4" />
        </Button>
      )}

      {/* Custom controls */}
      {controls && (
        <div
          className={cn(
            'absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent',
            'transition-opacity duration-300',
            showControls ? 'opacity-100' : 'opacity-0 pointer-events-none'
          )}
        >
          {/* Play/Pause button (center) */}
          <div className="absolute inset-0 flex items-center justify-center">
            <Button
              onClick={togglePlayPause}
              variant="ghost"
              size="lg"
              className={cn(
                'bg-black bg-opacity-50 text-white hover:bg-opacity-70 rounded-full',
                ageControlSizes[ageGroup]
              )}
              aria-label={isPlaying ? 'Pause video' : 'Play video'}
            >
              {isPlaying ? (
                <Pause className="h-6 w-6" />
              ) : (
                <Play className="h-6 w-6 ml-1" />
              )}
            </Button>
          </div>

          {/* Bottom controls */}
          <div className="absolute bottom-0 left-0 right-0 p-4 space-y-2">
            {/* Progress bar */}
            <div
              ref={progressRef}
              className="w-full h-2 bg-white bg-opacity-30 rounded-full cursor-pointer group"
              onClick={handleProgressClick}
              role="slider"
              aria-valuemin={0}
              aria-valuemax={100}
              aria-valuenow={progressPercentage}
              aria-label="Video progress"
            >
              <div
                className="h-full bg-teal-400 rounded-full transition-all duration-200 group-hover:bg-teal-300"
                style={{ width: `${progressPercentage}%` }}
              />
            </div>

            {/* Control buttons */}
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                {/* Mute button */}
                <Button
                  onClick={toggleMute}
                  variant="ghost"
                  size="sm"
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2"
                  aria-label={isMuted ? 'Unmute video' : 'Mute video'}
                >
                  {isMuted ? (
                    <VolumeX className="h-5 w-5" />
                  ) : (
                    <Volume2 className="h-5 w-5" />
                  )}
                </Button>

                {/* Time display */}
                <span className="text-white text-sm font-medium">
                  {formatTime(currentTime)} / {formatTime(videoDuration)}
                </span>
              </div>

              <div className="flex items-center space-x-2">
                {/* Fullscreen button */}
                <Button
                  onClick={toggleFullscreen}
                  variant="ghost"
                  size="sm"
                  className="text-white hover:bg-white hover:bg-opacity-20 p-2"
                  aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
                >
                  <Maximize className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Video title overlay (optional) */}
      {title && showControls && (
        <div className="absolute top-4 left-4 right-4">
          <h3 className="text-white text-lg font-semibold drop-shadow-lg line-clamp-2">
            {title}
          </h3>
        </div>
      )}
    </div>
  );
};

// Specialized video player for educational content feed
interface EducationalVideoPlayerProps extends VideoPlayerProps {
  topicBadge?: string;
  difficulty?: number;
  completionProgress?: number;
}

export const EducationalVideoPlayer: React.FC<EducationalVideoPlayerProps> = ({
  topicBadge,
  difficulty,
  completionProgress,
  ...props
}) => {
  return (
    <div className="relative">
      <VideoPlayer {...props} />
      
      {/* Topic badge */}
      {topicBadge && (
        <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
          {topicBadge}
        </div>
      )}
      
      {/* Difficulty indicator */}
      {difficulty && (
        <div className="absolute top-4 right-4 flex space-x-1">
          {Array.from({ length: 5 }, (_, i) => (
            <div
              key={i}
              className={cn(
                'w-2 h-2 rounded-full',
                i < difficulty ? 'bg-orange-400' : 'bg-white bg-opacity-30'
              )}
            />
          ))}
        </div>
      )}
      
      {/* Completion progress bar */}
      {completionProgress !== undefined && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-black bg-opacity-30">
          <div
            className="h-full bg-green-400 transition-all duration-300"
            style={{ width: `${completionProgress * 100}%` }}
          />
        </div>
      )}
    </div>
  );
};