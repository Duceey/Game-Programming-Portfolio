using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerCombat : MonoBehaviour
{
    [SerializeField] private float attackRange;
    [SerializeField] private int attackDamage;
    [SerializeField] private float attackDelay;
    [SerializeField] private float attackDamageDelay;

    private float attackTimer;
    private Animator anim;
    public Transform attackPoint;
    public LayerMask enemyLayer;
    private PlayerHealth playerHealth;


    private void Awake()
    {
        anim = GetComponent<Animator>();
        playerHealth = GetComponent<PlayerHealth>();
    }

    private void Update()
    {
        if (Input.GetKey(KeyCode.Mouse0) && CanAttack())
        {
            Attack();
        }
        attackTimer -= Time.deltaTime;
    }

    private void Attack()
    {
        attackTimer = attackDelay;

        anim.SetTrigger("attack");

        StartCoroutine(DamageEnemies());
    }

    IEnumerator DamageEnemies()
    {
        yield return new WaitForSeconds(attackDamageDelay);

        Collider2D[] hitEnemies = Physics2D.OverlapCircleAll(attackPoint.position, attackRange, enemyLayer);

        foreach (Collider2D enemy in hitEnemies)
        {
            enemy.GetComponent<Enemy>().TakeDamage(attackDamage);
        }
    }

    private bool CanAttack()
    {
        return attackTimer <= 0 && Alive();
    }

    private bool Alive()
    {
        return playerHealth.Alive();
    }

    public float GetAttackTimer()
    {
        return attackTimer;
    }
}
