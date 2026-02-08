# -*- coding: utf-8 -*-
"""
Database operations for Groups
"""

from db import fetch_all, execute
from utils.date_utils import get_current_persian_date, get_current_persian_datetime


def get_all_groups():
    """Fetch all groups, with leader full name when available"""
    query = """
        SELECT g.id, g.name, g.leader_member_id,
               COALESCE(m.full_name, '-') as leader_name,
               g.created_at
        FROM groups g
        LEFT JOIN members m ON g.leader_member_id = m.id
        ORDER BY g.id DESC
    """
    return fetch_all(query)


def get_group_by_id(group_id):
    """Fetch a single group by ID with leader name"""
    query = """
        SELECT g.id, g.name, g.leader_member_id,
               COALESCE(m.full_name, '-') as leader_name,
               g.created_at
        FROM groups g
        LEFT JOIN members m ON g.leader_member_id = m.id
        WHERE g.id = ?
    """
    result = fetch_all(query, (group_id,))
    return result[0] if result else None


def add_group(name, leader_member_id=None):
    """Add a new group with Persian date"""
    query = """
        INSERT INTO groups (name, leader_member_id, created_at)
        VALUES (?, ?, ?)
    """
    try:
        current_date = get_current_persian_datetime()
        group_id = execute(query, (name, leader_member_id, current_date))
        return True, group_id
    except Exception as e:
        return False, str(e)


def update_group(group_id, name, leader_member_id=None):
    """Update an existing group"""
    query = """
        UPDATE groups 
        SET name = ?, leader_member_id = ?
        WHERE id = ?
    """
    try:
        execute(query, (name, leader_member_id, group_id))
        return True, "گروه با موفقیت بروز شد"
    except Exception as e:
        return False, str(e)


def delete_group(group_id):
    """Delete a group (cascade deletes members)"""
    query = "DELETE FROM groups WHERE id = ?"
    try:
        execute(query, (group_id,))
        return True, "گروه با موفقیت حذف شد"
    except Exception as e:
        return False, str(e)


def group_exists(name, exclude_id=None):
    """Check if a group with this name already exists"""
    if exclude_id:
        query = "SELECT COUNT(*) as cnt FROM groups WHERE name = ? AND id != ?"
        result = fetch_all(query, (name, exclude_id))
    else:
        query = "SELECT COUNT(*) as cnt FROM groups WHERE name = ?"
        result = fetch_all(query, (name,))
    return result[0][0] > 0 if result else False
