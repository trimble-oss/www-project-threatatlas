import { useState } from 'react';
import { Upload } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ImportDrawioButtonProps {
  productId: number;
  onImportSuccess: (diagramId: number) => void;
}

export function ImportDrawioButton({ productId, onImportSuccess }: ImportDrawioButtonProps) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [diagramName, setDiagramName] = useState('');
  const [description, setDescription] = useState('');
  const [importing, setImporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      // Auto-fill diagram name from filename (without extension)
      const nameWithoutExt = selectedFile.name.replace(/\.(xml|drawio)$/, '');
      setDiagramName(nameWithoutExt);
      setError(null);
    }
  };

  const handleImport = async () => {
    if (!file || !diagramName) {
      setError('Please select a file and provide a diagram name');
      return;
    }

    try {
      setImporting(true);
      setError(null);

      const formData = new FormData();
      formData.append('file', file);
      formData.append('product_id', productId.toString());
      formData.append('name', diagramName);
      if (description) {
        formData.append('description', description);
      }

      const response = await fetch(`${API_BASE_URL}/api/diagrams/import-drawio`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Import failed');
      }

      const importedDiagram = await response.json();

      // Reset form
      setDialogOpen(false);
      setFile(null);
      setDiagramName('');
      setDescription('');

      // Notify parent
      onImportSuccess(importedDiagram.id);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to import diagram');
    } finally {
      setImporting(false);
    }
  };

  return (
    <>
      <Button variant="outline" size="sm" onClick={() => setDialogOpen(true)}>
        <Upload className="h-4 w-4 mr-2" />
        Import Draw.io
      </Button>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Import Draw.io Diagram</DialogTitle>
            <DialogDescription>
              Upload a Draw.io XML file to convert it into a ThreatAtlas diagram.
              Shapes will be automatically detected and mapped.
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="file">Draw.io File (.xml or .drawio)</Label>
              <Input
                id="file"
                type="file"
                accept=".xml,.drawio"
                onChange={handleFileChange}
                disabled={importing}
              />
              {file && (
                <p className="text-xs text-muted-foreground">
                  Selected: {file.name} ({(file.size / 1024).toFixed(1)} KB)
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="name">Diagram Name</Label>
              <Input
                id="name"
                value={diagramName}
                onChange={(e) => setDiagramName(e.target.value)}
                placeholder="Enter diagram name"
                disabled={importing}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description (Optional)</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe this diagram..."
                rows={3}
                disabled={importing}
              />
            </div>

            {error && (
              <div className="text-sm text-destructive bg-destructive/10 p-3 rounded">
                {error}
              </div>
            )}
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setDialogOpen(false)}
              disabled={importing}
            >
              Cancel
            </Button>
            <Button
              onClick={handleImport}
              disabled={!file || !diagramName || importing}
            >
              {importing ? 'Importing...' : 'Import Diagram'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
