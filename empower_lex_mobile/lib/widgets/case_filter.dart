import 'package:flutter/material.dart';

class CaseFilter extends StatelessWidget {
  final String selectedFilter;
  final Function(String) onFilterChanged;

  const CaseFilter({
    Key? key,
    required this.selectedFilter,
    required this.onFilterChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            _FilterChip(
              label: 'All',
              isSelected: selectedFilter == 'all',
              onSelected: (selected) => onFilterChanged('all'),
            ),
            SizedBox(width: 8),
            _FilterChip(
              label: 'Pending',
              isSelected: selectedFilter == 'pending',
              onSelected: (selected) => onFilterChanged('pending'),
            ),
            SizedBox(width: 8),
            _FilterChip(
              label: 'In Progress',
              isSelected: selectedFilter == 'in_progress',
              onSelected: (selected) => onFilterChanged('in_progress'),
            ),
            SizedBox(width: 8),
            _FilterChip(
              label: 'Completed',
              isSelected: selectedFilter == 'completed',
              onSelected: (selected) => onFilterChanged('completed'),
            ),
          ],
        ),
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool isSelected;
  final Function(bool) onSelected;

  const _FilterChip({
    Key? key,
    required this.label,
    required this.isSelected,
    required this.onSelected,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: onSelected,
      backgroundColor: Colors.grey[200],
      selectedColor: Theme.of(context).primaryColor.withOpacity(0.2),
      checkmarkColor: Theme.of(context).primaryColor,
      labelStyle: TextStyle(
        color: isSelected ? Theme.of(context).primaryColor : Colors.black87,
        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
      ),
    );
  }
} 