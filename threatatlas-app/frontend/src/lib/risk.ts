export function getSeverity(riskScore: number): 'low' | 'medium' | 'high' | 'critical' {
  if (riskScore >= 20) return 'critical';
  if (riskScore >= 12) return 'high';
  if (riskScore >= 6) return 'medium';
  return 'low';
}

export function getSeverityVariant(severity: string | null): 'destructive' | 'default' | 'secondary' | 'outline' {
  switch (severity) {
    case 'critical':
      return 'destructive';
    case 'high':
      return 'default';
    case 'medium':
      return 'secondary';
    case 'low':
      return 'outline';
    default:
      return 'outline';
  }
}

export function getSeverityColor(severity: string | null): string {
  switch (severity) {
    case 'critical':
      return 'hsl(0 84.2% 60.2%)';
    case 'high':
      return 'hsl(24.6 95% 53.1%)';
    case 'medium':
      return 'hsl(47.9 95.8% 53.1%)';
    case 'low':
      return 'hsl(142.1 76.2% 36.3%)';
    default:
      return 'hsl(240 5.9% 90%)';
  }
}

export function getSeverityClasses(severity: string | null): string {
  switch (severity) {
    case 'critical': return 'severity-critical';
    case 'high': return 'severity-high';
    case 'medium': return 'severity-medium';
    case 'low': return 'severity-low';
    default: return '';
  }
}

export function getSeverityStripeClass(severity: string | null): string {
  switch (severity) {
    case 'critical': return 'bg-red-500';
    case 'high': return 'bg-orange-500';
    case 'medium': return 'bg-amber-400';
    case 'low': return 'bg-green-500';
    default: return 'bg-border';
  }
}

export function getStatusClasses(status: string): string {
  switch (status) {
    case 'identified': return 'status-identified';
    case 'mitigated': return 'status-mitigated';
    case 'accepted': return 'status-accepted';
    case 'proposed': return 'status-proposed';
    case 'implemented': return 'status-implemented';
    case 'verified': return 'status-verified';
    default: return '';
  }
}
