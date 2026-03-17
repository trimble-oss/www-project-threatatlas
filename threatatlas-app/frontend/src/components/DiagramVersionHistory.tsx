import { useState, useEffect } from 'react';
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { Clock, ArrowUp, ArrowDown, Minus, RotateCcw, GitCompare } from 'lucide-react';
import { diagramVersionsApi } from '@/lib/api';
import { formatDistanceToNow } from 'date-fns';

interface DiagramVersionSummary {
  id: number;
  diagram_id: number;
  version_number: number;
  name: string;
  comment: string | null;
  created_at: string;
  node_count: number;
  edge_count: number;
  threat_count: number;
  total_risk_score: number;
}

interface DiagramVersionHistoryProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  diagramId: number;
  currentVersion: number;
  onRestore: () => void;
  onCompare?: (fromVersion: number, toVersion: number) => void;
}

export default function DiagramVersionHistory({
  open,
  onOpenChange,
  diagramId,
  currentVersion,
  onRestore,
  onCompare,
}: DiagramVersionHistoryProps) {
  const [versions, setVersions] = useState<DiagramVersionSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [restoreDialogOpen, setRestoreDialogOpen] = useState(false);
  const [selectedVersion, setSelectedVersion] = useState<number | null>(null);
  const [selectedForCompare, setSelectedForCompare] = useState<number[]>([]);

  useEffect(() => {
    if (open) {
      loadVersions();
    }
  }, [open, diagramId]);

  const loadVersions = async () => {
    setLoading(true);
    try {
      const response = await diagramVersionsApi.list(diagramId);
      setVersions(response.data);
    } catch (error) {
      console.error('Failed to load versions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRestoreClick = (versionNumber: number) => {
    setSelectedVersion(versionNumber);
    setRestoreDialogOpen(true);
  };

  const handleRestoreConfirm = async () => {
    if (selectedVersion === null) return;

    try {
      await diagramVersionsApi.restore(diagramId, selectedVersion);
      setRestoreDialogOpen(false);
      setSelectedVersion(null);
      onRestore();
      loadVersions();
    } catch (error) {
      console.error('Failed to restore version:', error);
    }
  };

  const handleCompareToggle = (versionNumber: number) => {
    setSelectedForCompare(prev => {
      if (prev.includes(versionNumber)) {
        return prev.filter(v => v !== versionNumber);
      } else if (prev.length < 2) {
        return [...prev, versionNumber];
      } else {
        // Replace the first selected version
        return [prev[1], versionNumber];
      }
    });
  };

  const handleCompare = () => {
    if (selectedForCompare.length === 2 && onCompare) {
      const [v1, v2] = selectedForCompare.sort((a, b) => a - b);
      onCompare(v1, v2);
    }
  };

  const getRiskTrend = (current: DiagramVersionSummary, previous?: DiagramVersionSummary) => {
    if (!previous) return null;

    const delta = current.total_risk_score - previous.total_risk_score;

    if (delta > 0) {
      return <ArrowUp className="h-4 w-4 text-red-500" />;
    } else if (delta < 0) {
      return <ArrowDown className="h-4 w-4 text-green-500" />;
    }
    return <Minus className="h-4 w-4 text-gray-400" />;
  };

  return (
    <>
      <Sheet open={open} onOpenChange={onOpenChange}>
        <SheetContent className="!w-full sm:!max-w-[700px] p-0 flex flex-col">
          <div className="px-4 pt-4 pb-4 border-b">
            <SheetHeader className="space-y-3">
              <SheetTitle className="text-2xl font-bold">Version History</SheetTitle>
            </SheetHeader>
          </div>

          <div className="flex-1 overflow-y-auto px-4 py-4">
            {selectedForCompare.length === 2 && (
              <div className="mb-4">
                <Button
                  onClick={handleCompare}
                  variant="outline"
                  className="w-full"
                >
                  <GitCompare className="h-4 w-4 mr-2" />
                  Compare Versions {selectedForCompare[0]} and {selectedForCompare[1]}
                </Button>
              </div>
            )}

            <div className="space-y-4">
            {loading ? (
              <div className="flex items-center justify-center p-8">
                <p className="text-sm text-muted-foreground">Loading versions...</p>
              </div>
            ) : versions.length === 0 ? (
              <div className="flex items-center justify-center p-8">
                <p className="text-sm text-muted-foreground">No versions yet</p>
              </div>
            ) : (
              versions.map((version, index) => {
                const previousVersion = versions[index + 1];
                const isSelected = selectedForCompare.includes(version.version_number);

                return (
                  <div key={version.id}>
                    <div
                      className={`border rounded-lg p-4 hover:bg-muted/30 transition-colors ${
                        isSelected ? 'border-primary bg-accent' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-2">
                          <h3 className="text-sm font-semibold">Version {version.version_number}</h3>
                          {version.version_number === currentVersion && (
                            <Badge variant="default">Current</Badge>
                          )}
                        </div>
                        <div className="flex items-center gap-1">
                          {getRiskTrend(version, previousVersion)}
                        </div>
                      </div>

                      <div className="space-y-3">
                        <div className="flex items-center text-muted-foreground text-sm">
                          <Clock className="h-3 w-3 mr-1" />
                          {formatDistanceToNow(new Date(version.created_at), { addSuffix: true })}
                        </div>

                        {version.comment && (
                          <p className="text-sm italic border-l-2 border-primary pl-2 text-muted-foreground">
                            {version.comment}
                          </p>
                        )}

                        <div className="h-px bg-border" />

                        <div className="grid grid-cols-2 gap-2 text-xs text-muted-foreground">
                          <div>Nodes: {version.node_count}</div>
                          <div>Edges: {version.edge_count}</div>
                          <div>Threats: {version.threat_count}</div>
                          <div>Risk Score: {version.total_risk_score}</div>
                        </div>
                      </div>

                      <div className="flex gap-2 mt-4">
                        {version.version_number !== currentVersion && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleRestoreClick(version.version_number)}
                          >
                            <RotateCcw className="h-3 w-3 mr-1" />
                            Restore
                          </Button>
                        )}
                        <Button
                          size="sm"
                          variant={isSelected ? "default" : "ghost"}
                          onClick={() => handleCompareToggle(version.version_number)}
                        >
                          <GitCompare className="h-3 w-3 mr-1" />
                          {isSelected ? 'Selected' : 'Compare'}
                        </Button>
                      </div>
                    </div>
                    {index < versions.length - 1 && <div className="h-px bg-border my-4" />}
                  </div>
                );
              })
            )}
            </div>
          </div>
        </SheetContent>
      </Sheet>

      <AlertDialog open={restoreDialogOpen} onOpenChange={setRestoreDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Restore Version?</AlertDialogTitle>
            <AlertDialogDescription>
              This will restore the diagram to version {selectedVersion}. A new version will be created
              preserving the current state. This action can be undone by restoring another version.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={handleRestoreConfirm}>
              Restore Version
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}
