"""
Database Operations Module.

Helper functions for saving and retrieving data from the database.
"""

from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
import logging

from src.models import JobListing, JobAnalysis, SearchHistory
from src.state import Job, Job_Feedback
from src.structure_outputs import Job_Summary

logger = logging.getLogger(__name__)


def save_job_listing(session: Session, job: Job) -> JobListing:
    """
    Save or update a job listing in the database.
    
    Args:
        session: Database session
        job: Job object from workflow state
        
    Returns:
        JobListing: Saved job listing
    """
    # Check if job already exists
    existing_job = session.get(JobListing, job.id)
    
    if existing_job:
        logger.debug(f"Job {job.id} already exists, skipping")
        return existing_job
    
    # Create new job listing
    job_listing = JobListing(
        id=job.id,
        title=job.title,
        company_name=job.companyName,
        location=job.location,
        apply_url=job.applyUrl,
        description=job.description,
        posted_date=job.postedDate
    )
    
    session.add(job_listing)
    logger.debug(f"Saved job listing: {job.id}")
    return job_listing


def save_job_analysis(
    session: Session,
    job_id: str,
    summary: Job_Summary,
    feedback: Job_Feedback
) -> JobAnalysis:
    """
    Save job analysis (summary and feedback) to database.
    
    Args:
        session: Database session
        job_id: Job ID
        summary: Job summary object
        feedback: Job feedback object
        
    Returns:
        JobAnalysis: Saved analysis
    """
    # Check if analysis already exists for this job
    statement = select(JobAnalysis).where(JobAnalysis.job_id == job_id)
    existing_analysis = session.exec(statement).first()
    
    if existing_analysis:
        # Update existing analysis
        existing_analysis.summary = summary.job_info
        existing_analysis.skills = summary.job_skills
        existing_analysis.similarity_score = feedback.similarity
        existing_analysis.feedback = feedback.feedback
        logger.debug(f"Updated analysis for job {job_id}")
        return existing_analysis
    
    # Create new analysis
    analysis = JobAnalysis(
        job_id=job_id,
        summary=summary.job_info,
        similarity_score=feedback.similarity,
        feedback=feedback.feedback
    )
    analysis.skills = summary.job_skills  # Uses the property setter
    
    session.add(analysis)
    logger.debug(f"Saved analysis for job {job_id}")
    return analysis


def save_search_history(
    session: Session,
    user_query: str,
    resume_name: str
) -> SearchHistory:
    """
    Save search history to database.
    
    Args:
        session: Database session
        user_query: User's search query
        resume_name: Name of the resume file
        
    Returns:
        SearchHistory: Saved search history
    """
    search_history = SearchHistory(
        user_query=user_query,
        resume_name=resume_name
    )
    
    session.add(search_history)
    logger.debug(f"Saved search history: {user_query}")
    return search_history


def get_all_jobs(session: Session, limit: int = 50) -> List[JobListing]:
    """
    Retrieve all job listings from database.
    
    Args:
        session: Database session
        limit: Maximum number of jobs to return
        
    Returns:
        List of JobListing objects
    """
    statement = select(JobListing).limit(limit)
    jobs = session.exec(statement).all()
    return list(jobs)


def get_job_with_analysis(session: Session, job_id: str) -> Optional[JobListing]:
    """
    Retrieve a job listing with its analysis.
    
    Args:
        session: Database session
        job_id: Job ID
        
    Returns:
        JobListing with analysis relationship loaded, or None
    """
    job = session.get(JobListing, job_id)
    return job


def get_search_history(session: Session, limit: int = 20) -> List[SearchHistory]:
    """
    Retrieve search history.
    
    Args:
        session: Database session
        limit: Maximum number of records to return
        
    Returns:
        List of SearchHistory objects
    """
    statement = select(SearchHistory).order_by(SearchHistory.timestamp.desc()).limit(limit)
    history = session.exec(statement).all()
    return list(history)


def save_workflow_results(
    session: Session,
    user_query: str,
    resume_name: str,
    jobs: List[Job],
    job_summaries: List[Job_Summary],
    job_feedbacks: List[Job_Feedback]
) -> None:
    """
    Save complete workflow results to database.
    
    Args:
        session: Database session
        user_query: User's search query
        resume_name: Resume file name
        jobs: List of scraped jobs
        job_summaries: List of job summaries
        job_feedbacks: List of job feedbacks
    """
    try:
        # Save search history
        save_search_history(session, user_query, resume_name)
        
        # Save job listings
        for job in jobs:
            save_job_listing(session, job)
        
        # Create dictionaries for easy lookup
        summaries_dict = {s.id: s for s in job_summaries}
        feedbacks_dict = {f.id: f for f in job_feedbacks}
        
        # Save analyses
        for job_id in summaries_dict.keys():
            if job_id in feedbacks_dict:
                save_job_analysis(
                    session,
                    str(job_id),
                    summaries_dict[job_id],
                    feedbacks_dict[job_id]
                )
        
        # Commit all changes
        session.commit()
        logger.info(f"Successfully saved workflow results: {len(jobs)} jobs, {len(job_summaries)} analyses")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error saving workflow results: {str(e)}", exc_info=True)
        raise
