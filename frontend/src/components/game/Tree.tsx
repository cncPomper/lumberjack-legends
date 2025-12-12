import React from 'react';
import { useGame, BranchSide } from '@/contexts/GameContext';
import { cn } from '@/lib/utils';

interface BranchProps {
  side: BranchSide;
  isShaking: boolean;
}

const Branch: React.FC<BranchProps> = ({ side, isShaking }) => {
  if (side === 'none') return null;

  return (
    <div
      className={cn(
        "absolute w-20 h-6 branch",
        side === 'left' ? "-left-16 branch-left" : "-right-16 branch-right",
        isShaking && "animate-tree-shake"
      )}
      style={{
        top: '50%',
        transform: 'translateY(-50%)',
        background: 'linear-gradient(90deg, hsl(25 50% 22%) 0%, hsl(25 50% 28%) 50%, hsl(25 50% 22%) 100%)',
      }}
    >
      {/* Branch leaves */}
      <div
        className={cn(
          "absolute -top-3 w-12 h-10 rounded-full",
          side === 'left' ? "-left-8" : "-right-8"
        )}
        style={{
          background: 'radial-gradient(ellipse at center, hsl(120 40% 35%) 0%, hsl(120 40% 25%) 70%)',
        }}
      />
    </div>
  );
};

interface TreeSegmentProps {
  branch: BranchSide;
  index: number;
  isShaking: boolean;
}

const TreeSegment: React.FC<TreeSegmentProps> = ({ branch, index, isShaking }) => {
  return (
    <div
      className={cn(
        "relative w-16 h-12 tree-trunk",
        isShaking && "animate-tree-shake"
      )}
      style={{
        animationDelay: `${index * 20}ms`,
      }}
    >
      <Branch side={branch} isShaking={isShaking} />
    </div>
  );
};

const Tree: React.FC = () => {
  const { treeSegments, isChopping } = useGame();

  return (
    <div className="relative flex flex-col items-center">
      {/* Tree top/leaves */}
      <div
        className="w-32 h-24 rounded-full mb-2 animate-float"
        style={{
          background: 'radial-gradient(ellipse at center, hsl(120 45% 40%) 0%, hsl(120 40% 25%) 80%)',
          boxShadow: '0 10px 30px hsl(120 40% 20% / 0.5)',
        }}
      />
      
      {/* Tree segments */}
      <div className="flex flex-col-reverse">
        {treeSegments.map((segment, index) => (
          <TreeSegment
            key={segment.id}
            branch={segment.branch}
            index={index}
            isShaking={isChopping && index === 0}
          />
        ))}
      </div>

      {/* Tree base/stump */}
      <div
        className="w-24 h-8 rounded-b-lg"
        style={{
          background: 'linear-gradient(180deg, hsl(25 50% 25%) 0%, hsl(25 45% 18%) 100%)',
        }}
      />
    </div>
  );
};

export default Tree;
