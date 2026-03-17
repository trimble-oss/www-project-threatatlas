import { useState, useEffect } from 'react';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Trash2 } from 'lucide-react';
import ThreatManagement from '@/components/ThreatManagement';

interface ElementPropertiesSheetProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  selectedElement: { id: string; type: 'node' | 'edge'; label: string; nodeType?: string } | null;
  diagramId: number | null;
  activeModelId: number | null;
  activeModelFrameworkId: number | null;
  onRename: (name: string) => void;
  onDelete: () => void;
}

export default function ElementPropertiesSheet({
  open,
  onOpenChange,
  selectedElement,
  diagramId,
  activeModelId,
  activeModelFrameworkId,
  onRename,
  onDelete,
}: ElementPropertiesSheetProps) {
  const [elementName, setElementName] = useState('');

  useEffect(() => {
    if (selectedElement) {
      setElementName(selectedElement.label);
    }
  }, [selectedElement]);

  const handleRename = () => {
    onRename(elementName);
  };

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="!w-full sm:!max-w-[700px] p-0 flex flex-col">
        <div className="px-4 pt-4 pb-4 border-b">
          <SheetHeader className="space-y-3">
            <SheetTitle className="text-2xl font-bold">
              {selectedElement?.label || 'Element Properties'}
            </SheetTitle>
            <SheetDescription className="flex items-center gap-2">
              {selectedElement?.nodeType && (
                <>
                  <Badge variant="secondary" className="capitalize">
                    {selectedElement.nodeType}
                  </Badge>
                  <span className="text-muted-foreground/60">•</span>
                </>
              )}
              <span>Configure properties, threats, and mitigations</span>
            </SheetDescription>
          </SheetHeader>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
            {/* Element Name Section */}
            <div className="space-y-3">
              <h3 className="text-sm font-semibold">Element Information</h3>
              <div className="flex items-center gap-3">
                <div className="flex-1 space-y-2">
                  <Label className="text-sm font-medium">Name</Label>
                  <Input
                    value={elementName}
                    onChange={(e) => setElementName(e.target.value)}
                    onBlur={handleRename}
                    placeholder="Enter element name"
                  />
                </div>

                {selectedElement?.nodeType && (
                  <div className="space-y-2">
                    <Label className="text-sm font-medium">Type</Label>
                    <div className="flex items-center h-10">
                      <Badge variant="outline" className="capitalize">
                        {selectedElement.nodeType}
                      </Badge>
                    </div>
                  </div>
                )}

                {selectedElement?.id && (
                  <div className="space-y-2">
                    <Label className="text-sm font-medium">ID</Label>
                    <div className="flex items-center h-10">
                      <code className="text-xs bg-muted px-2 py-1 rounded">
                        {selectedElement.id}
                      </code>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="h-px bg-border" />

            {/* Threats Section */}
            {diagramId && selectedElement && (
              <div className="space-y-3">
                <h3 className="text-sm font-semibold">Threats & Mitigations</h3>
                {activeModelId && activeModelFrameworkId ? (
                  <ThreatManagement
                    diagramId={diagramId}
                    activeModelId={activeModelId}
                    modelFrameworkId={activeModelFrameworkId}
                    elementId={selectedElement.id}
                    elementType={selectedElement.type}
                  />
                ) : (
                  <div className="text-sm text-muted-foreground bg-muted/50 p-4 rounded-lg border border-dashed">
                    Please select a model from the toolbar to manage threats and mitigations.
                  </div>
                )}
              </div>
            )}

            <div className="h-px bg-border" />

            {/* Danger Zone */}
            <div className="space-y-3 p-4 rounded-lg border border-destructive/50 bg-destructive/5">
              <div className="flex items-center gap-2">
                <Trash2 className="h-4 w-4 text-destructive" />
                <h3 className="text-sm font-semibold">Danger Zone</h3>
              </div>
              <p className="text-xs text-muted-foreground">
                Delete this element and all associated threats and mitigations. This action cannot be undone.
              </p>
              <Button
                variant="destructive"
                size="sm"
                className="w-full"
                onClick={onDelete}
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Delete Element
              </Button>
            </div>
          </div>
      </SheetContent>
    </Sheet>
  );
}
