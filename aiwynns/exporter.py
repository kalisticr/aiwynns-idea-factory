"""
Exporter module for exporting data to various formats
"""

import json
import csv
import yaml
from pathlib import Path
from typing import List, Dict


class Exporter:
    """Export database to various formats"""

    def __init__(self, database):
        self.db = database

    def export(self, type: str = 'all', format: str = 'json', output_path: str = None):
        """
        Export data to file

        Args:
            type: 'batches', 'stories', or 'all'
            format: 'json', 'csv', or 'yaml'
            output_path: Path to output file
        """
        data = self._gather_data(type)

        if format == 'json':
            self._export_json(data, output_path)
        elif format == 'csv':
            self._export_csv(data, output_path, type)
        elif format == 'yaml':
            self._export_yaml(data, output_path)
        else:
            raise ValueError(f"Unknown format: {format}")

    def _gather_data(self, type: str) -> Dict:
        """Gather data based on type"""
        data = {}

        if type in ['batches', 'all']:
            batches = self.db.get_all_batches()
            # Remove content to keep export clean
            data['batches'] = [
                {k: v for k, v in batch.items() if k not in ['content', 'concepts']}
                for batch in batches
            ]

        if type in ['stories', 'all']:
            stories = self.db.get_all_stories()
            # Remove content to keep export clean
            data['stories'] = [
                {k: v for k, v in story.items() if k != 'content'}
                for story in stories
            ]

        return data

    def _export_json(self, data: Dict, output_path: str):
        """Export to JSON"""
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def _export_yaml(self, data: Dict, output_path: str):
        """Export to YAML"""
        with open(output_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    def _export_csv(self, data: Dict, output_path: str, type: str):
        """Export to CSV"""
        with open(output_path, 'w', newline='') as f:
            if type == 'batches' or (type == 'all' and 'batches' in data):
                self._export_batches_csv(data.get('batches', []), f)
            elif type == 'stories' or (type == 'all' and 'stories' in data):
                self._export_stories_csv(data.get('stories', []), f)
            elif type == 'all':
                # Export both to same CSV with type column
                self._export_combined_csv(data, f)

    def _export_batches_csv(self, batches: List[Dict], file):
        """Export batches to CSV"""
        if not batches:
            return

        fieldnames = ['batch_id', 'date_generated', 'genre', 'tropes', 'count', 'status', 'location', 'llm_model']
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for batch in batches:
            # Convert lists to strings for CSV
            row = batch.copy()
            if isinstance(row.get('tropes'), list):
                row['tropes'] = ', '.join(row['tropes'])
            if isinstance(row.get('genre'), list):
                row['genre'] = ', '.join(row['genre'])
            writer.writerow(row)

    def _export_stories_csv(self, stories: List[Dict], file):
        """Export stories to CSV"""
        if not stories:
            return

        fieldnames = ['story_id', 'title', 'genre', 'subgenre', 'tropes', 'status', 'date_created', 'target_length']
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')

        writer.writeheader()
        for story in stories:
            row = story.copy()
            if isinstance(row.get('tropes'), list):
                row['tropes'] = ', '.join(row['tropes'])
            if isinstance(row.get('genre'), list):
                row['genre'] = ', '.join(row['genre'])
            writer.writerow(row)

    def _export_combined_csv(self, data: Dict, file):
        """Export combined data to CSV"""
        fieldnames = ['type', 'id', 'title', 'genre', 'date', 'status', 'count_or_length']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        # Add batches
        for batch in data.get('batches', []):
            writer.writerow({
                'type': 'batch',
                'id': batch.get('batch_id'),
                'title': f"Batch {batch.get('batch_id')}",
                'genre': batch.get('genre'),
                'date': batch.get('date_generated'),
                'status': batch.get('status'),
                'count_or_length': batch.get('count')
            })

        # Add stories
        for story in data.get('stories', []):
            writer.writerow({
                'type': 'story',
                'id': story.get('story_id'),
                'title': story.get('title'),
                'genre': story.get('genre'),
                'date': story.get('date_created'),
                'status': story.get('status'),
                'count_or_length': story.get('target_length')
            })
