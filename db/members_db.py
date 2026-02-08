# -*- coding: utf-8 -*-
"""
Database operations for Members
"""

from db import fetch_all, execute
from utils.date_utils import get_current_persian_date, get_current_persian_datetime


def get_all_members():
    """Fetch all members with their group name"""
    query = """
        SELECT m.id, m.full_name, m.group_id, g.name as group_name,
               m.phone, m.is_active, m.joined_at
        FROM members m
        LEFT JOIN groups g ON m.group_id = g.id
        ORDER BY m.id DESC
    """
    return fetch_all(query)


def get_member_by_id(member_id):
    """Fetch a single member by ID"""
    query = """
        SELECT m.id, m.full_name, m.group_id, g.name as group_name,
               m.phone, m.is_active, m.joined_at
        FROM members m
        LEFT JOIN groups g ON m.group_id = g.id
        WHERE m.id = ?
    """
    result = fetch_all(query, (member_id,))
    return result[0] if result else None


def get_members_by_group(group_id):
    """Fetch all members in a specific group"""
    query = """
        SELECT id, full_name, phone, is_active, joined_at
        FROM members
        WHERE group_id = ?
        ORDER BY full_name
    """
    return fetch_all(query, (group_id,))


def add_member(full_name, group_id, phone=None):
    """Add a new member with Persian date"""
    query = """
        INSERT INTO members (full_name, group_id, phone, joined_at)
        VALUES (?, ?, ?, ?)
    """
    try:
        joined_date = get_current_persian_date()
        member_id = execute(query, (full_name, group_id, phone, joined_date))
        return True, member_id
    except Exception as e:
        return False, str(e)


def update_member(member_id, full_name, group_id, phone=None, is_active=1):
    """Update an existing member"""
    query = """
        UPDATE members 
        SET full_name = ?, group_id = ?, phone = ?, is_active = ?
        WHERE id = ?
    """
    try:
        execute(query, (full_name, group_id, phone, is_active, member_id))
        return True, "عضو با موفقیت بروز شد"
    except Exception as e:
        return False, str(e)


def delete_member(member_id):
    """Delete a member (cascade deletes related data)"""
    query = "DELETE FROM members WHERE id = ?"
    try:
        execute(query, (member_id,))
        return True, "عضو با موفقیت حذف شد"
    except Exception as e:
        return False, str(e)


def member_exists(full_name, exclude_id=None):
    """Check if a member with this name already exists"""
    if exclude_id:
        query = "SELECT COUNT(*) as cnt FROM members WHERE full_name = ? AND id != ?"
        result = fetch_all(query, (full_name, exclude_id))
    else:
        query = "SELECT COUNT(*) as cnt FROM members WHERE full_name = ?"
        result = fetch_all(query, (full_name,))
    return result[0][0] > 0 if result else False


def toggle_member_active(member_id, is_active):
    """Toggle member active status"""
    query = "UPDATE members SET is_active = ? WHERE id = ?"
    try:
        execute(query, (is_active, member_id))
        return True, "وضعیت عضو با موفقیت بروز شد"
    except Exception as e:
        return False, str(e)
