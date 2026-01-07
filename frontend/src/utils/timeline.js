/**
 * Timeline Template Engine
 * Calculates project milestones based on anchor dates and offsets
 * Similar to Folio by Amitree
 */

// Built-in Timeline Templates
export const TIMELINE_TEMPLATES = {
    roofing_standard: {
        id: 'roofing_standard',
        name: 'Standard Roof Replacement',
        description: 'Typical timeline for residential roof replacement',
        anchorField: 'first_estimate_signed_date',
        anchorLabel: 'Estimate Signed',
        steps: [
            {
                name: 'Estimate Signed',
                offsetDays: 0,
                relatedField: 'first_estimate_signed_date',
                isAnchor: true
            },
            {
                name: 'Permits Filed',
                offsetDays: 2,
                relatedField: 'file_date',
                description: 'Submit permit application'
            },
            {
                name: 'Deposit Received',
                offsetDays: 5,
                relatedField: null, // Internal milestone
                description: 'Customer deposit payment due'
            },
            {
                name: 'Materials Ordered',
                offsetDays: 7,
                relatedField: null,
                description: 'Order roofing materials'
            },
            {
                name: 'Permit Approved',
                offsetDays: 10,
                relatedField: null,
                description: 'Permit approval expected'
            },
            {
                name: 'Job Start',
                offsetDays: 14,
                relatedField: null,
                description: 'Crew arrives on site'
            },
            {
                name: 'Job Complete',
                offsetDays: 17,
                relatedField: null,
                description: 'Work finished'
            },
            {
                name: 'Final Inspection',
                offsetDays: 20,
                relatedField: 'warranty_and_permit_closed',
                description: 'City/county inspection'
            },
            {
                name: 'Final Payment',
                offsetDays: 22,
                relatedField: 'paid_in_full_date',
                description: 'Customer final payment due'
            }
        ]
    },

    roofing_repair: {
        id: 'roofing_repair',
        name: 'Roof Repair',
        description: 'Expedited timeline for repairs',
        anchorField: 'first_estimate_signed_date',
        anchorLabel: 'Estimate Signed',
        steps: [
            {
                name: 'Estimate Signed',
                offsetDays: 0,
                relatedField: 'first_estimate_signed_date',
                isAnchor: true
            },
            {
                name: 'Materials Ordered',
                offsetDays: 1,
                relatedField: null
            },
            {
                name: 'Repair Scheduled',
                offsetDays: 3,
                relatedField: null
            },
            {
                name: 'Repair Complete',
                offsetDays: 5,
                relatedField: null
            },
            {
                name: 'Payment Received',
                offsetDays: 7,
                relatedField: 'paid_in_full_date'
            }
        ]
    },

    storm_restoration: {
        id: 'storm_restoration',
        name: 'Storm Restoration',
        description: 'Insurance claim timeline',
        anchorField: 'first_estimate_signed_date',
        anchorLabel: 'Estimate Signed',
        steps: [
            {
                name: 'Estimate Signed',
                offsetDays: 0,
                relatedField: 'first_estimate_signed_date',
                isAnchor: true
            },
            {
                name: 'Insurance Claim Filed',
                offsetDays: 1,
                relatedField: null
            },
            {
                name: 'Adjuster Meeting',
                offsetDays: 7,
                relatedField: null
            },
            {
                name: 'Insurance Approval',
                offsetDays: 14,
                relatedField: null
            },
            {
                name: 'Permits Filed',
                offsetDays: 16,
                relatedField: 'file_date'
            },
            {
                name: 'Deductible Paid',
                offsetDays: 18,
                relatedField: null
            },
            {
                name: 'Materials Ordered',
                offsetDays: 20,
                relatedField: null
            },
            {
                name: 'Job Start',
                offsetDays: 25,
                relatedField: null
            },
            {
                name: 'Job Complete',
                offsetDays: 30,
                relatedField: null
            },
            {
                name: 'Final Inspection',
                offsetDays: 33,
                relatedField: 'warranty_and_permit_closed'
            },
            {
                name: 'Insurance Payment',
                offsetDays: 40,
                relatedField: 'paid_in_full_date'
            }
        ]
    }
};

/**
 * Add days to a date, skipping weekends
 */
export function addBusinessDays(date, days) {
    let result = new Date(date);
    let daysAdded = 0;

    while (daysAdded < days) {
        result.setDate(result.getDate() + 1);
        const dayOfWeek = result.getDay();

        // Skip Saturday (6) and Sunday (0)
        if (dayOfWeek !== 0 && dayOfWeek !== 6) {
            daysAdded++;
        }
    }

    return result;
}

/**
 * Push date to next Monday if it falls on weekend
 */
export function avoidWeekend(date) {
    const dayOfWeek = date.getDay();

    if (dayOfWeek === 6) { // Saturday -> Monday
        date.setDate(date.getDate() + 2);
    } else if (dayOfWeek === 0) { // Sunday -> Monday
        date.setDate(date.getDate() + 1);
    }

    return date;
}

/**
 * Calculate timeline dates based on template and anchor date
 */
export function applyTimeline(job, template, useBusinessDays = true) {
    // Get anchor date from job
    const anchorFieldValue = job[template.anchorField];

    if (!anchorFieldValue) {
        throw new Error(`Anchor date "${template.anchorField}" not found in job data`);
    }

    // Convert to Date object (handle Unix timestamp or date string)
    const anchorDate = typeof anchorFieldValue === 'number'
        ? new Date(anchorFieldValue * 1000)
        : new Date(anchorFieldValue);

    // Calculate each step's date
    const timeline = template.steps.map((step, index) => {
        let calculatedDate;

        if (step.isAnchor) {
            calculatedDate = new Date(anchorDate);
        } else if (useBusinessDays) {
            calculatedDate = addBusinessDays(anchorDate, step.offsetDays);
        } else {
            calculatedDate = new Date(anchorDate);
            calculatedDate.setDate(calculatedDate.getDate() + step.offsetDays);
            calculatedDate = avoidWeekend(calculatedDate);
        }

        // Check if this step has an actual date in job data (user override)
        const actualDate = step.relatedField && job[step.relatedField]
            ? (typeof job[step.relatedField] === 'number'
                ? new Date(job[step.relatedField] * 1000)
                : new Date(job[step.relatedField]))
            : null;

        // Determine status
        const now = new Date();
        let status = 'pending';

        if (actualDate) {
            status = 'completed';
        } else if (calculatedDate < now) {
            status = 'overdue';
        } else if (calculatedDate.toDateString() === now.toDateString()) {
            status = 'today';
        }

        return {
            id: `step-${index}`,
            name: step.name,
            description: step.description,
            offsetDays: step.offsetDays,
            calculatedDate,
            actualDate,
            relatedField: step.relatedField,
            status,
            isSynced: !!step.relatedField,
            isAnchor: step.isAnchor || false
        };
    });

    return timeline;
}

/**
 * Apply cascading update when a date changes
 */
export function cascadeTimelineUpdate(timeline, changedStepIndex, newDate, originalDate) {
    // Calculate the shift in days
    const daysDiff = Math.round((newDate - originalDate) / (1000 * 60 * 60 * 24));

    if (daysDiff === 0) return timeline;

    // Update all subsequent steps
    return timeline.map((step, index) => {
        if (index <= changedStepIndex) {
            // Don't change steps before or at the changed step
            return index === changedStepIndex
                ? { ...step, actualDate: newDate, calculatedDate: newDate }
                : step;
        }

        // Shift subsequent steps by the same number of days
        const shiftedDate = new Date(step.calculatedDate);
        shiftedDate.setDate(shiftedDate.getDate() + daysDiff);

        return {
            ...step,
            calculatedDate: avoidWeekend(shiftedDate),
            actualDate: step.actualDate
                ? (() => {
                    const shiftedActual = new Date(step.actualDate);
                    shiftedActual.setDate(shiftedActual.getDate() + daysDiff);
                    return avoidWeekend(shiftedActual);
                })()
                : null
        };
    });
}

/**
 * Get timeline for job (from database or calculate fresh)
 */
export async function getJobTimeline(job, templateId = 'roofing_standard') {
    const template = TIMELINE_TEMPLATES[templateId];

    if (!template) {
        throw new Error(`Template "${templateId}" not found`);
    }

    return applyTimeline(job, template);
}

export default {
    TIMELINE_TEMPLATES,
    applyTimeline,
    cascadeTimelineUpdate,
    getJobTimeline,
    addBusinessDays,
    avoidWeekend
};
