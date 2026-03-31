"""
Unit tests for octo/core.py
Tests for: timestamps, text wrapping, CSV export, clipboard, error handling
"""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import os

# Add octo package to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from octo import core


class TestFileTimestamp:
    """Tests for file last-modified timestamp feature"""
    
    @patch('octo.core._get_json')
    def test_get_file_last_modified_success(self, mock_get_json):
        """Test successful fetch of file modification time"""
        mock_get_json.return_value = (200, [
            {
                "commit": {
                    "committer": {
                        "date": "2025-01-15T14:30:45Z"
                    }
                }
            }
        ])
        
        result = core.get_file_last_modified("owner", "repo", "file.py")
        
        assert result is not None
        assert "2025-01-15" in result
        assert "UTC" in result
    
    @patch('octo.core._get_json')
    def test_get_file_last_modified_no_commits(self, mock_get_json):
        """Test handling when file has no commits"""
        mock_get_json.return_value = (200, [])
        
        result = core.get_file_last_modified("owner", "repo", "file.py")
        
        assert result is None


class TestTextWrapping:
    """Tests for description text wrapping"""
    
    def test_format_description_none(self):
        """Test handling of None description"""
        result = core._format_description(None)
        assert result == "No description"
    
    def test_format_description_short(self):
        """Test short description passes through"""
        desc = "A simple Python library"
        result = core._format_description(desc, max_width=80)
        assert desc in result
    
    def test_format_description_long(self):
        """Test long description is wrapped"""
        desc = "A " * 50 + "very long description"
        result = core._format_description(desc, max_width=40)
        lines = result.split('\n')
        assert len(lines) > 1


class TestClipboard:
    """Tests for clipboard functionality"""
    
    @patch('subprocess.Popen')
    def test_copy_to_clipboard_success(self, mock_popen):
        """Test successful clipboard copy"""
        mock_process = MagicMock()
        mock_process.communicate.return_value = None
        mock_popen.return_value = mock_process
        
        result = core.copy_to_clipboard("test content")
        
        assert result is True


class TestCSVExport:
    """Tests for CSV export functionality"""
    
    @patch('builtins.open', create=True)
    @patch('csv.DictWriter')
    def test_export_contributors_csv(self, mock_writer, mock_open):
        """Test CSV export"""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_csv_writer = MagicMock()
        mock_writer.return_value = mock_csv_writer
        
        contributors = [
            {'login': 'user1', 'contributions': 100},
            {'login': 'user2', 'contributions': 50}
        ]
        
        core.export_contributors_csv("owner", "repo", contributors, "/tmp")
        
        mock_csv_writer.writeheader.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])