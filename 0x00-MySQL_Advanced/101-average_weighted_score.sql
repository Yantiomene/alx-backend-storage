-- creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users u
  INNER JOIN (
    SELECT user_id, SUM(p.weight * c.score) AS total_weighted_score, SUM(p.weight) AS total_weight
    FROM projects p
    INNER JOIN corrections c ON c.project_id = p.id
    GROUP BY user_id
  ) AS scores ON u.id = scores.user_id
  SET u.average_score = scores.total_weighted_score / scores.total_weight;
END; //
DELIMITER ;
